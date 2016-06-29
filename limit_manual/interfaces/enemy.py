from flask import render_template, request

from .. import app, get_connection

# Gather basic information on an enemy
# that is not related to any version specifically
class EnemyBase(object):
    def __init__(self,name,conn):
        self.name = name
        cur = conn.cursor()
        cur.execute('''SELECT base_id, description, image FROM enemies
                       WHERE name=%s''', (name,))
        result = cur.fetchone()
        self.base_id = result[0]
        self.description = result[1]
        self.image = result[2]

    def __repr__(self):
        return '<Enemy Base: {0}>'.format(self.name)

    def all_versions(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT ver_name FROM enemy_versions
                       WHERE base_id=%s''', (self.base_id,))
        result = { r[0] for r in cur.fetchall() }
        conn.close()

        return result

# Version-specific info about an enemy
# Includes location, stats, formations, items, ...
class Enemy(EnemyBase):
    def __init__(self,enemy_name,ver_name,conn):
        EnemyBase.__init__(self,enemy_name,conn)

        cur = conn.cursor()
        cur.execute('''SELECT base_id, ver_id, ver_name,
                       level, hp, mp,
                       attack, defense,
                       magic_attack, magic_defense,
                       defense_pct, magic_defense_pct,
                       dexterity, luck,
                       exp, ap, gil
                       FROM enemy_versions
                       WHERE base_id=%s AND ver_name=%s''', (self.base_id,ver_name))
        result = cur.fetchone()

        self.version = ver_name

        self.ver_id = result[1]

        self.stats = {
            'level' : result[3],
            'hp'    : result[4],
            'mp'    : result[5],
            'attack'    : result[6],
            'defense'   : result[7],
            'magic_attack'  : result[8],
            'magic_defense' : result[9],
            'defense_pct'       : result[10],
            'magic_defense_pct' : result[11],
            'dexterity' : result[12],
            'luck'      : result[13]
        }
        self.rewards = {
            'exp'   : result[14],
            'ap'    : result[15],
            'gil'   : result[16]
        }

        # Find the names of all other versions of this enemy
        self.other_versions = self.all_versions() - { self.version }

        # Fill list of items that can be gotten from this enemy
        self.items = { 'drop': [], 'steal': [], 'morph': None }
        cur.execute('''SELECT get_method, item_name, get_chance
                       FROM enemy_items
                       WHERE enemy_ver_id=%s''', (self.ver_id,))
        for item in cur.fetchall():
            if item[0] == 'D':
                self.items['drop'].append( (item[1], item[2]) )
            elif item[0] == 'S':
                self.items['steal'].append( (item[1], item[2]) )
            else:
                self.items['morph'] = item[1]

        self.elemental_modifiers = []
        cur.execute('''SELECT element, modifier
                       FROM enemy_elemental_modifiers
                       WHERE enemy_ver_id=%s''', (self.ver_id,))
        for mod in cur.fetchall():
            self.elemental_modifiers.append( { 'element': mod[0], 'modifier': mod[1] } )

        cur.execute('''SELECT status
                       FROM enemy_status_immunities
                       WHERE enemy_ver_id=%s''', (self.ver_id,))
        self.status_immunities = { r[0] for r in cur.fetchall() }

    def __repr__(self):
        return '<Enemy: {0}; Version: {1}>'.format(self.name,self.version)

    def get_formations(self):
        formations = []

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT DISTINCT formation_id
                       FROM formation_enemies
                       WHERE enemy_ver_id=%s''', (self.ver_id,))
        formation_ids = [ row[0] for row in cur.fetchall() ]

        for f_id in formation_ids:
            this_f = { 'id': f_id, 'locations': {}, 'enemy_rows': {} }

            cur.execute('''SELECT loc, sub_loc
                           FROM formation_locations
                           WHERE formation_id=%s''', (f_id,))
            for row in cur.fetchall():
                if row[0] not in this_f['locations'].keys():
                    this_f['locations'][row[0]] = []
                this_f['locations'][row[0]].append(row[1])

            cur.execute('''SELECT name, ver_name, row_num, position
                           FROM formation_enemies JOIN
                                (SELECT name, ver_name, ver_id
                                 FROM enemies AS e JOIN enemy_versions AS ev ON e.base_id=ev.base_id) as enemy_info
                                ON formation_enemies.enemy_ver_id=enemy_info.ver_id
                           WHERE formation_id=%s''', (f_id,))
            for row in cur.fetchall():
                if row[2] not in this_f['enemy_rows'].keys():
                    this_f['enemy_rows'][row[2]] = []
                this_f['enemy_rows'][row[2]].append((row[0],row[1]))

            formations.append(this_f)

        conn.close()
        return formations

# Route declaration for specific enemy pages
@app.route('/enemies/<name>')
def enemy(name):
    version_name = request.args.get('version', None)

    if version_name == None: version_name = "Normal"

    conn = get_connection()
    enemy = Enemy(name,version_name,conn)
    conn.close()

    return render_template('enemies/enemy.j2',
                           enemy=enemy,
                           formations=enemy.get_formations())

# Route declation for the list of all enemies
@app.route('/enemies')
@app.route('/enemies/all')
def all_enemies():
    # from ..relations.formation import get_formation_ids, get_locations

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT base_id, name FROM enemies")
    results = cur.fetchall()

    enemies = []

    for result in results:
        info = { 'name': result[1] }
        cur.execute("SELECT ver_name FROM enemy_versions WHERE base_id=%s", (result[0],))
        info['versions'] = { row[0] for row in cur.fetchall() }

        enemies.append(info)

    conn.close()
    return render_template('enemies/all_enemies.j2', enemies=enemies)
