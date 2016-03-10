from flask import render_template

from .. import app, db

from ..relations import item as ItemRelations

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

class Weapon(Item):
    @staticmethod
    def db_reference(name):
        return ItemRelations.Weapon.query.filter_by(name=name).one_or_none()

    def __init__(self,name):
        Item.__init__(self,name)

        db_row = self.db_reference(self.name)
        # Weapon properties
        self.attack = db_row.attack
        self.hit_pct = db_row.hit_pct
        self.magic_bonus = db_row.magic_bonus
        self.element = db_row.element
        # Materia-related properties
        self.linked_slots = db_row.linked_slots
        self.single_slots = db_row.single_slots
        self.growth_rate = db_row.growth_rate

    def __repr__(self):
        return '<{0}>'.format(self.name)

    @staticmethod
    def create(name,attack,hit_pct,magic_bonus,element,
               linked_slots,single_slots,growth_rate):
        # Make sure the item exists in the general items table
        uid = Item.db_reference(name).uid if Item.db_reference(name) != None else Item.create(name)
        # Add the weapon to the weapons table
        db.session.add(ItemRelations.Weapon(uid, name,
                                            attack,hit_pct,
                                            magic_bonus,
                                            element,
                                            linked_slots,
                                            single_slots,
                                            growth_rate))
        db.session.commit()

    def create_many(weapons):
        for weapon in weapons:
            uid = Item.db_reference(weapon.name).uid if Item.db_reference(weapon.name) != None else Item.create(weapon.name)
            db.session.add(ItemRelations.Weapon(uid,**weapon))
        db.session.commit()

class Armor(Item):
    @staticmethod
    def db_reference(name):
        return ItemRelations.Armor.query.filter_by(name=name).one_or_none()

    def __init__(self,name):
        Item.__init__(self,name)

        db_row = self.db_reference(self.name)
        # Armor properties
        self.defense = db_row.defense
        self.magic_defense = db_row.magic_defense
        self.defense_pct = db_row.defense_pct
        self.magic_defense_pct = db_row.magic_defense_pct
        # Materia-related properties
        self.linked_slots = db_row.linked_slots
        self.single_slots = db_row.single_slots
        self.growth_rate = db_row.growth_rate

    def __repr__(self):
        return '<{0}>'.format(self.name)

    @staticmethod
    def create(name,defense,magic_defense,defense_pct,magic_defense_pct,
               linked_slots,single_slots,growth_rate):
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
            uid = Item.db_reference(armor.name).uid if Item.db_reference(armor.name) != None else Item.create(armor.name)
            db.session.add(ItemRelations.Armor(uid,**armor))
        db.session.commit()

@app.route('/items')
@app.route('/items/all')
def all_items():
    items = [ Item(item.name,item.uid) for item in ItemRelations.Item.query.all() ]

    return render_template('items/all_items.j2', items=items)
