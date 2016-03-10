from .. import db

class Item(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Item: {0!s}>'.format(self.name)

class Weapon(db.Model):
    # Basic info
    uid = db.Column(db.Integer, db.ForeignKey('item.uid'),
                        primary_key=True)
    name = db.Column(db.String(20))
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

    def __init__(self, item_id, name='Buster Sword',
                 attack=18, hit_pct=96, magic_bonus=2,
                 element='Cut',
                 linked_slots=1, single_slots=0,
                 growth_rate=1):
        self.uid = item_id
        self.name = name
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

    def __init__(self, item_id, name='Bronze Bangle',
                 defense=8, magic_defense=0,
                 defense_pct=0,magic_defense_pct=0,
                 linked_slots=0,single_slots=0,
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
