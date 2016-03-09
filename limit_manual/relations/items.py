from .. import app, db

class Item(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Item: {0!s}>'.format(self.name)

class Weapon(db.Model):
    item_id = db.Column(db.Integer, db.ForeignKey('item.uid'),
                        primary_key=True)
    name = db.Column(db.String(20))
    item = db.relationship('Item', db.backref('weapon', lazy='dynamic'))
    attack = db.Column(db.Integer)
    hit_pct = db.Column(db.Integer)
    magic_bonus = db.Column(db.Integer)
    growth_rate = db.Column(db.Integer)
    single_slots = db.Column(db.Integer)
    linked_slots = db.Column(db.Integer)
    element = db.Column(db.String(16))

class Armor(db.Model):
    item_id = db.Column(db.Integer, db.ForeignKey('item.uid'))
    name = db.Column(db.String(20))
    item = db.relationship('Item', db.backref('armor', lazy='dynamic'))
