from flask import render_template, request

from .. import app, get_connection
from .common_relations import get_description

class Ability(object):
    def get_statuses(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT mode, chance FROM ability_status_info
                          WHERE ability_id=?''', (self.uid,))
        info = cur.fetchone()
        cur.execute('''SELECT status FROM ability_status_list
                          WHERE ability_id=?''', (self.uid,))
        status_list = [ row[0] for row in cur.fetchall() ]
        conn.close()

        self.statuses = {
            'list': status_list,
            'mode': info[0],
            'chance': info[1]
        }

    def get_damage(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT formula, power, piercing
                          FROM ability_damage
                          WHERE ability_id=?''', (self.uid,))
        damage = cur.fetchone()
        conn.close()

        self.damage = {
            'formula': damage[0],
            'power': damage[1],
            'piercing': damage[2],
            'physical': damage[0] == 'Physical'
        }

        self.get_damage_string()

    def get_damage_string(self):
        if self.damage['formula'] == 'Max HP%':
            if self.damage['power'] == 32:
                self.damage_text = 'Restore HP to full'
            else:
                self.damage_text = 'Heal damage equal to {0}% of Max HP'.format(100*self.damage['power']//32)
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

            if self.element != 'None':
                damage_properties.append('{0}-elemental'.format(self.element))

            self.damage_text = 'Deals {0} damage'.format(' '.join(damage_properties).lower())

            if self.target_all or self.num_attacks > 1:
                self.damage_text = self.damage_text + ' to each target'

    def __init__(self,name=None,uid=None):
        conn = get_connection()
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

        ability_notes = []
        if ability_row[4]: #has_notes
            cur.execute('''SELECT note_text FROM ability_notes
                           WHERE ability_id=?''', (self.uid,))
            ability_notes.extend([ row[0] for row in cur.fetchall() ])

        if ability_row[5]: # has_info
            cur.execute("SELECT * FROM ability_info WHERE uid=?", (self.uid,))
            info_row = cur.fetchone()
            self.hit_formula = info_row[1]
            self.accuracy = info_row[2]
            self.element = info_row[3]
            self.friendly = info_row[4]
            self.target_all = info_row[5]
            self.target_random = info_row[6]
            self.num_attacks = info_row[7]
            self.split = info_row[8]

            if info_row[9]: # has_statuses
                self.get_statuses()
            else: self.statuses = None

            if info_row[10]: # has_damage
                self.get_damage()
            else: self.damage = None

            if self.target_all:
                ability_notes.append('targets entire party')
            elif self.target_random:
                if self.num_attacks == 1:
                    ability_notes.append('selects one target randomly')
                else:
                    ability_notes.append('selects a random target {0} times'.format(self.num_attacks))

            if self.split == False:
                ability_notes.append('full power multi-target')

        if len(ability_notes) > 0:
            self.notes_string = ', '.join(ability_notes)
        else:
            self.notes_string = None

        self.in_game_description = get_description(ability_row[2],"Ability",self.uid)

        conn.close()

class Spell(Ability):
    def __init__(self,name):
        Ability.__init__(self,name)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT * FROM magic_info
                       WHERE ability_id=?''', (self.uid,))
        row = cur.fetchone()
        self.mp_cost = row[1]
        self.spell_type = row[2]
        self.reflectable = row[3]
        conn.close()

class Summon(Ability):
    def __init__(self,name):
        Ability.__init__(self,name)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT * FROM summon_info
                       WHERE ability_id=?''', (self.uid,))
        info_row = cur.fetchone()
        self.mp_cost = info_row[1]

        cur.execute('''SELECT attack_id FROM summon_attacks
                       WHERE summon_id=?''', (self.uid,))
        self.attacks = [ Ability(uid=r[0]) for r in cur.fetchmany(info_row[2]) ]
        conn.close()


@app.route('/abilities')
@app.route('/abilities/all')
def all_actions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, category FROM abilities;")

    spells = []
    summons = []

    for row in cur.fetchall():
        if row[1] == "Magic":
            spells.append(Spell(row[0]))
        elif row[1] == "Summon":
            summons.append(Summon(row[0]))

    spell_content = render_template('abilities/magic/simple_spells.j2',
                                    spells=spells)
    summon_content = render_template('abilities/summons/simple_summons.j2',
                                     summons=summons)

    return render_template('abilities/all_abilities.j2',
                           spell_content=spell_content,
                           summon_content=summon_content)

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

    for _spell in [ r[0] for r in cur.fetchall() ]:
        spell = Spell(_spell)
        if spell.spell_type == "Restore":
            restore.append(spell)
        elif spell.spell_type == "Attack":
            attack.append(spell)
        elif spell.spell_type == "Indirect":
            indirect.append(spell)
        else:
            other.append(spell)

    return render_template('abilities/magic/magic.j2', detail=detail,
                           restore=restore, attack=attack,
                           indirect=indirect, other=other)

@app.route('/abilities/summons')
def all_summons():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM abilities WHERE category=?",("Summon",))

    summons = [ Summon(r[0]) for r in cur.fetchall() ]

    return render_template('abilities/summons/summons.j2',
                           summons=summons)
