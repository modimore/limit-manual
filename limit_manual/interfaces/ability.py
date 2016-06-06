from flask import render_template, request

from .. import app, get_connection
from .common_relations import get_description

class Ability(object):
    def get_statuses(self,conn):
        cur = conn.cursor()
        cur.execute('''SELECT mode, chance FROM ability_status_info
                          WHERE ability_id=?''', (self.uid,))
        info = cur.fetchone()
        if info == None:
            self.statuses = None
        else:
            cur.execute('''SELECT status FROM ability_status_list
                              WHERE ability_id=?''', (self.uid,))
            status_list = [ row[0] for row in cur.fetchall() ]

            self.statuses = {
                'list': status_list,
                'mode': info[0],
                'chance': info[1]
            }

    def get_damage(self,conn):
        cur = conn.cursor()
        cur.execute('''SELECT formula, power, piercing
                          FROM ability_damage
                          WHERE ability_id=?''', (self.uid,))
        damage_row = cur.fetchone()

        if damage_row == None:
            self.damage = None
        else:
            self.damage = {
                'formula': damage_row[0],
                'power': damage_row[1],
                'piercing': damage_row[2] == 1,
                'physical': damage_row[0] == 'Physical'
            }

            self.get_damage_string()

    def get_damage_string(self):
        if self.damage['formula'] == 'Max HP%':
            if self.damage['power'] == 32:
                self.damage_text = 'Restore HP to full'
            else:
                self.damage_text = 'Heal damage equal to {0}% of Max HP'.format(100*self.damage['power']//32)
        elif self.damage['formula'] == 'Caster\'s HP':
            self.damage_text = 'Heal damage equal to caster\'s current HP'
        elif self.damage['formula'] == 'Cure':
            if self.damage['power'] < 20: level = 'light'
            elif self.damage['power'] < 40: level = 'moderate'
            else: level = 'major'

            self.damage_text = 'Heal a {0} amount of damage'.format(level)
        elif self.damage['formula'] == 'HP%':
            self.damage_text = 'Deal damage equal to {0}% of target\'s current HP'.format(100*self.damage['power']//32)
        else:
            damage_properties = []
            if self.damage['power'] < 20: damage_properties.append('light')
            elif self.damage['power'] < 40: damage_properties.append('moderate')
            elif self.damage['power'] < 80: damage_properties.append('high')
            else: damage_properties.append('heavy')

            if len(self.elements) == 0:
                pass
            elif len(self.elements) == 1:
                damage_properties.append('{0}-elemental'.format(self.elements[0]))
            else:
                damage_properties.append('multi-elemental')

            self.damage_text = 'Deals {0} damage'.format(' '.join(damage_properties).lower())

            if self.targeting_type == 'All' or self.repeat > 1:
                self.damage_text = self.damage_text + ' to each target'

    def __init__(self,conn,name=None,uid=None):
        cur = conn.cursor()

        if uid != None:
            cur.execute("SELECT * FROM abilities WHERE uid=?", (uid,))
        else:
            cur.execute("SELECT * FROM abilities WHERE name=?", (name,))
        ability_row = cur.fetchone()

        # common attributes of all abilities
        self.uid = ability_row[0]
        self.name = ability_row[1]
        self.category = ability_row[3]

        self.elements = []
        self.targeting_type = 'Choice'
        self.repeat = 1

        self.friendly = False
        self.no_split = False

        ability_notes = []
        if ability_row[4]: #has_notes
            cur.execute('''SELECT note_text FROM ability_notes
                           WHERE ability_id=?''', (self.uid,))
            ability_notes.extend([ row[0] for row in cur.fetchall() ])

        if ability_row[5]: # has_info
            # cur.execute("SELECT * FROM ability_info WHERE uid=?", (self.uid,))
            # info_row = cur.fetchone()
            # self.hit_formula = info_row[1]
            # self.accuracy = info_row[2]
            # self.element = info_row[3]
            # self.friendly = info_row[4] == 1
            # self.target_all = info_row[5] == 1
            # self.target_random = info_row[6] == 1
            # self.num_attacks = info_row[7]
            # self.split = info_row[8] == 1

            cur.execute('''SELECT type, value FROM ability_property_map
                           WHERE ability_id=?''', (self.uid,))
            for row in cur.fetchall():
                if row[0] == 'Hit Formula':
                    self.hit_formula = row[1]
                elif row[0] == 'Accuracy':
                    self.accuracy = row[1]
                elif row[0] == 'Element':
                    self.elements.append(row[1])
                elif row[0] == 'Target':
                    self.targeting_type = row[1]
                elif row[0] == 'Repeat':
                    self.repeat = int(row[1])

            cur.execute('''SELECT type FROM ability_property_set
                           WHERE ability_id=?''', (self.uid,))

            for row in cur.fetchall():
                if row[0] == 'Friendly':
                    self.friendly = True
                elif row[0] == 'No-split':
                    self.no_split = True

            self.get_statuses(conn)

            self.get_damage(conn)

        if len(ability_notes) > 0:
            self.notes_string = ', '.join(ability_notes)
        else:
            self.notes_string = None

        self.in_game_description = get_description(ability_row[2],"Ability",self.uid)

class Spell(Ability):
    def __init__(self,conn,name):
        Ability.__init__(self,conn,name)

        cur = conn.cursor()
        cur.execute('''SELECT * FROM magic_info
                       WHERE ability_id=?''', (self.uid,))
        row = cur.fetchone()
        self.mp_cost = row[1]
        self.spell_type = row[2]
        self.reflectable = row[3] == 1

class Summon(Ability):
    def __init__(self,conn,name):
        Ability.__init__(self,conn,name)

        cur = conn.cursor()
        cur.execute('''SELECT * FROM summon_info
                       WHERE ability_id=?''', (self.uid,))
        info_row = cur.fetchone()
        self.mp_cost = info_row[1]

        cur.execute('''SELECT attack_id FROM summon_attacks
                       WHERE summon_id=?''', (self.uid,))
        self.attacks = [ Ability(conn,uid=r[0]) for r in cur.fetchmany(info_row[2]) ]

class EnemySkill(Ability):
    def __init__(self,conn,name):
        Ability.__init__(self,conn,name=name)

        cur = conn.cursor()
        cur.execute('''SELECT * FROM enemy_skill_info
                       WHERE ability_id=?''', (self.uid,))
        row = cur.fetchone()
        self.mp_cost = row[1]
        self.reflectable = row[2]
        self.missable = row[3]
        self.manip_only = row[4]

        cur.execute('''SELECT enemy_name FROM enemy_skill_users
                       WHERE ability_id=?''', (self.uid,))
        self.users = [ row[0] for row in cur.fetchall() ]

class Command(Ability):
    def __init__(self,conn,name):
        Ability.__init__(self,conn,name=name)


@app.route('/abilities')
@app.route('/abilities/all')
def all_actions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, category FROM abilities;")

    spells = []
    summons = []
    eskills = []
    commands = []

    for row in cur.fetchall():
        if row[1] == "Command":
            commands.append(Command(conn,name=row[0]))
        elif row[1] == "Magic":
            spells.append(Spell(conn,name=row[0]))
        elif row[1] == "Summon":
            summons.append(Summon(conn,name=row[0]))
        elif row[1] == "Enemy Skill":
            eskills.append(EnemySkill(conn,name=row[0]))

    conn.close()

    return render_template('abilities/all_abilities.j2',
                           commands=commands,
                           spells=spells,
                           summons=summons,
                           eskills=eskills)

@app.route('/abilities/magic')
@app.route('/abilities/spells')
def all_magic():
    detail = (request.args.get('display',None) in ['Detail','detail'])

    restore = []
    attack = []
    indirect = []
    other = []

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM abilities WHERE category=?",("Magic",))

    for spell_name in [ r[0] for r in cur.fetchall() ]:
        spell = Spell(conn,name=spell_name)
        if spell.spell_type == "Restore":
            restore.append(spell)
        elif spell.spell_type == "Attack":
            attack.append(spell)
        elif spell.spell_type == "Indirect":
            indirect.append(spell)
        else:
            other.append(spell)

    conn.close()

    return render_template('abilities/magic/magic.j2', detail=detail,
                           restore=restore, attack=attack,
                           indirect=indirect, other=other)

@app.route('/abilities/summons')
def all_summons():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM abilities WHERE category=?",("Summon",))

    summons = [ Summon(conn,name=r[0]) for r in cur.fetchall() ]

    conn.close()

    return render_template('abilities/summons/summons.j2',
                           summons=summons)

@app.route('/abilities/enemy skills')
@app.route('/abilities/eskills')
def all_eskills():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM abilities WHERE category=?", ("Enemy Skill", ))

    eskills = [ EnemySkill(conn,name=r[0]) for r in cur.fetchall() ]

    conn.close()

    return render_template('abilities/enemy_skills/eskills.j2',
                           eskills=eskills)

@app.route('/abilities/commands')
def all_commands():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM abilities WHERE category=?", ("Command",))

    commands = [ Command(conn,name=r[0]) for r in cur.fetchall() ]

    conn.close()

    return render_template('abilities/commands/commands.j2',
                           commands=commands)
