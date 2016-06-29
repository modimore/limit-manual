from flask import render_template

from .. import app, get_connection
from .common_relations import get_description

# Representation of the basic item type
class Item(object):
    def __init__(self,name,uid=None):
        self.name = name
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT uid, item_type, descr_id
                       FROM items
                       WHERE name=%s;''', (self.name,))
        row = cur.fetchone()
        self.uid = row[0]
        self.item_type = row[1]
        descr_id = row[2]
        conn.close()

        self.description = get_description(descr_id,'item',self.uid)

    def extract(self, with_uid=False):
        result = { 'name': self.name, 'type': self.item_type }
        if with_uid: result['uid'] = self.uid
        return result

    @staticmethod
    def extract_all(with_uid=False):
        all_items = []
        for item in ItemRelations.Item.query.all():
            all_items.append(Item(item.name,item.uid).extract(with_uid))
        return all_items

# Representation of a weapon
class Weapon(Item):
    def __init__(self,name):
        Item.__init__(self,name)

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('''SELECT growth_rate, linked_slots, single_slots,
                           attack, hit_pct, magic_bonus, element, wielder
                           FROM weapons
                           WHERE uid=%s;''', (self.uid,))
            row = cur.fetchone()

            # Materia-related properties
            self.growth_rate = row[0]
            self.linked_slots = row[1]
            self.single_slots = row[2]
            # Weapon properties
            self.wielder = row[7]
            self.attack = row[3]
            self.hit_pct = row[4]
            self.magic_bonus = row[5]
            self.element = row[6]

    def __repr__(self):
        return '<{0}>'.format(self.name)

class Armor(Item):
    def __init__(self,name):
        Item.__init__(self,name)

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('''SELECT growth_rate, linked_slots, single_slots,
                                  defense, magic_defense,
                                  defense_pct, magic_defense_pct
                           FROM armor WHERE uid=%s;''', (self.uid,))
            row = cur.fetchone()

            # Materia-related properties
            self.growth_rate = row[0]
            self.linked_slots = row[1]
            self.single_slots = row[2]
            # Armor properties
            self.defense = row[3]
            self.magic_defense = row[4]
            self.defense_pct = row[5]
            self.magic_defense_pct = row[6]


    def __repr__(self):
        return '<{0}>'.format(self.name)

@app.route('/items')
@app.route('/items/all')
def all_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM items;")
    item_names = [ row[0] for row in cur.fetchall() ]
    conn.close()

    items = {
        'general': [],
        'weapons': [],
        'armor': []
    }

    for name in item_names:
        item = Item(name)
        if item.item_type == 'Weapon':
            items['weapons'].append(item)
        elif item.item_type == 'Armor':
            items['armor'].append(item)
        else:
            items['general'].append(item)

    return render_template('items/all_items.j2', items=items)

@app.route('/items/weapons')
@app.route('/weapons')
def all_weapons():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM weapons;")
    weapon_names = [ row[0] for row in cur.fetchall() ]
    conn.close()

    weapons = [ Weapon(name) for name in weapon_names ]
    return render_template('items/weapons.j2', weapons=weapons)

@app.route('/items/armor')
@app.route('/armor')
def all_armor():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM armor;")
    armor_names = [ row[0] for row in cur.fetchall() ]
    conn.close()

    armor = [ Armor(name) for name in armor_names ]
    return render_template('items/armor.j2', armor=armor)
