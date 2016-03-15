from .. import db

class Item(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Item: {0!s}>'.format(self.name)

'''
class ItemSubclass(db.Model):
    uid = db.Column(db.Integer, db.ForeignKey('item.uid'),
                    primary_key=True)
    name = db.Column(db.String(20))
'''

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

'''
class Restorative(db.Model):
    uid = db.Column(db.Integer, db.ForeignKey('item.uid'),
                    primary_key=True)
    name = db.Column(db.String(20))
    item = db.relationship('Item', backref=db.backref('restorative', lazy='Dynamic'))
    stat = db.Column(db.String(2), primary_key=True)
    amt = db.Column(db.Integer)

    def __init__(self, item_id, name, stat, amt):
        self.uid = item_id
        self.name = name
        self.stat = stat
        self.amt = amt

    def __repr__(self):
        return '<Restorative {0!s} {1!s}>'.format(self.name,self.stat)
'''
