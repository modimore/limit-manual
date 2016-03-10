from flask import render_template

from .. import app, db

from ..relations import item as ItemRelations

# Representation of the basic item type
class Item(object):
    @staticmethod
    def db_reference(name):
        return ItemRelations.Item.query.filter_by(name=name).one_or_none()

    def __init__(self,name,uid=None):
        self.name = name
        self.uid = uid if uid != None else self.db_reference(self.name).uid

    @staticmethod
    def create(name):
        new_item = ItemRelations.Item(name)
        db.session.add(new_item)
        db.session.commit()
        return new_item.uid

    @staticmethod
    def create_many(names):
        for name in names:
            db.session.add(ItemRelations.Item(name))
        db.session.commit()

# Representation of a weapon
class Weapon(Item):
    @staticmethod
    def db_reference(name):
        return ItemRelations.Weapon.query.filter_by(name=name).one_or_none()

    def __init__(self,name):
        Item.__init__(self,name)

        ref = self.db_reference(self.name)
        # Weapon properties
        self.wielder = ref.wielder
        self.attack = ref.attack
        self.hit_pct = ref.hit_pct
        self.magic_bonus = ref.magic_bonus
        self.element = ref.element
        # Materia-related properties
        self.linked_slots = ref.linked_slots
        self.single_slots = ref.single_slots
        self.growth_rate = ref.growth_rate

    def __repr__(self):
        return '<{0}>'.format(self.name)

    @staticmethod
    def create(name,wielder,attack,hit_pct,magic_bonus,element,
               linked_slots,single_slots,growth_rate=1):
        # Make sure the item exists in the general items table
        uid = Item.db_reference(name).uid if Item.db_reference(name) != None else Item.create(name)
        # Add the weapon to the weapons table
        db.session.add(ItemRelations.Weapon(uid,name,wielder,
                                            attack,hit_pct,
                                            magic_bonus,
                                            element,
                                            linked_slots,
                                            single_slots,
                                            growth_rate))
        db.session.commit()

    def create_many(weapons):
        for weapon in weapons:
            uid = Item.db_reference(weapon['name']).uid if Item.db_reference(weapon['name']) != None else Item.create(weapon['name'])
            db.session.add(ItemRelations.Weapon(uid,**weapon))
        db.session.commit()

class Armor(Item):
    @staticmethod
    def db_reference(name):
        return ItemRelations.Armor.query.filter_by(name=name).one_or_none()

    def __init__(self,name):
        Item.__init__(self,name)

        ref = self.db_reference(self.name)
        # Armor properties
        self.defense = ref.defense
        self.magic_defense = ref.magic_defense
        self.defense_pct = ref.defense_pct
        self.magic_defense_pct = ref.magic_defense_pct
        # Materia-related properties
        self.linked_slots = ref.linked_slots
        self.single_slots = ref.single_slots
        self.growth_rate = ref.growth_rate

    def __repr__(self):
        return '<{0}>'.format(self.name)

    @staticmethod
    def create(name,defense,magic_defense,defense_pct,magic_defense_pct,
               linked_slots,single_slots,growth_rate=1):
        # Make sure the item exists in the general items table
        uid = Item.db_reference(name).uid if Item.db_reference(name) != None else Item.create(name)
        # Add the weapon to the weapons table
        db.session.add(ItemRelations.Armor(uid, name,
                                           defense,
                                           magic_defense,
                                           defense_pct,
                                           magic_defense_pct,
                                           linked_slots,single_slots,
                                           growth_rate))
        db.session.commit()

    def create_many(armor_list):
        for armor in armor_list:
            uid = Item.db_reference(armor['name']).uid if Item.db_reference(armor['name']) != None else Item.create(armor['name'])
            db.session.add(ItemRelations.Armor(uid,**armor))
        db.session.commit()

@app.route('/items')
@app.route('/items/all')
def all_items():
    items = [ Item(item.name,item.uid) for item in ItemRelations.Item.query.all() ]

    return render_template('items/all_items.j2', items=items)

@app.route('/items/weapons')
@app.route('/weapons')
def all_weapons():
    _weapons = ItemRelations.Weapon.query.with_entities(ItemRelations.Weapon.name)\
                                         .order_by(ItemRelations.Weapon.wielder)\
                                         .all()
    weapons = [ Weapon(wp.name) for wp in _weapons ]

    return render_template('items/weapons.j2', weapons=weapons)

@app.route('/items/armor')
@app.route('/armor')
def all_armor():
    _armor = ItemRelations.Armor.query.with_entities(ItemRelations.Armor.name).all()
    armor = [ Armor(ar.name) for ar in _armor ]

    return render_template('items/armor.j2', armor=armor)
