from .. import db
from .miscellaneous import DescriptionFormat

class Item(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    item_type = db.Column(db.String(20))
    descr_id = db.Column(db.Integer, db.ForeignKey('description_format.uid'))

    def __init__(self,name,item_type,descr_id=1):
        self.name = name
        self.item_type = item_type
        self.descr_id = descr_id

    def __repr__(self):
        return '<Item: {0!s}>'.format(self.name)

class Weapon(db.Model):
    # Basic info
    uid = db.Column(db.Integer, db.ForeignKey('item.uid'),
                        primary_key=True)
    name = db.Column(db.String(20))
    wielder = db.Column(db.String(10))
    item = db.relationship('Item', backref=db.backref('weapon', lazy='dynamic'))
    # Weapons and Armor
    growth_rate = db.Column(db.Integer)
    linked_slots = db.Column(db.Integer)
    single_slots = db.Column(db.Integer)
    # Weapon-specific
    attack = db.Column(db.Integer)
    hit_pct = db.Column(db.Integer)
    magic_bonus = db.Column(db.Integer)
    element = db.Column(db.String(16))

    def __init__(self, item_id, name, wielder,
                 attack, hit_pct, magic_bonus,
                 element,
                 linked_slots, single_slots,
                 growth_rate=1):
        self.uid = item_id
        self.name = name
        self.wielder = wielder
        self.attack = attack
        self.hit_pct = hit_pct
        self.magic_bonus = magic_bonus
        self.element = element
        self.linked_slots = linked_slots
        self.single_slots = single_slots
        self.growth_rate = growth_rate

    def __repr__(self):
        return '<Weapon {0!s}>'.format(self.name)

class Armor(db.Model):
    # Basic info
    uid = db.Column(db.Integer, db.ForeignKey('item.uid'),
                    primary_key=True)
    name = db.Column(db.String(20))
    item = db.relationship('Item', backref=db.backref('armor', lazy='dynamic'))
    # Weapons and Armor
    growth_rate = db.Column(db.Integer)
    linked_slots = db.Column(db.Integer)
    single_slots = db.Column(db.Integer)
    # Armor-specific
    defense = db.Column(db.Integer)
    magic_defense = db.Column(db.Integer)
    defense_pct = db.Column(db.Integer)
    magic_defense_pct = db.Column(db.Integer)

    def __init__(self, item_id, name,
                 defense, magic_defense,
                 defense_pct,magic_defense_pct,
                 linked_slots,single_slots,
                 growth_rate=1):
        self.uid = item_id
        self.name = name
        self.defense = defense
        self.magic_defense = magic_defense
        self.defense_pct = defense_pct
        self.magic_defense_pct = magic_defense_pct
        self.linked_slots = linked_slots
        self.single_slots = single_slots
        self.growth_rate = growth_rate

    def __repr__(self):
        return '<Armor {0!s}>'.format(self.name)
