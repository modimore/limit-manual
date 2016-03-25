from .. import db
from .miscellaneous import DescriptionFormat

class Action(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    category = db.Column(db.String(20))
    descr_id = db.Column(db.Integer, db.ForeignKey('description_format.uid'))

    def __init__(self,name,category,descr_id=0):
        self.name = name
        self.category = category

    def __repr__(self):
        return '<\"{1}\"-type action {0}>'.format(self.name,self.category)

class SpellInfo(db.Model):
    action_id = db.Column(db.Integer, db.ForeignKey('action.uid'),
                          primary_key=True)
    spell_type = db.Column(db.String(12))
    mp_cost = db.Column(db.Integer)
    reflectable = db.Column(db.Boolean)


    def __init__(self,action_id,mp_cost,spell_type='Unassigned',reflectable=False):
        self.action_id = action_id
        self.spell_type = spell_type
        self.mp_cost = mp_cost
        self.reflectable = reflectable

class ActionEffect(db.Model):
    action_id = db.Column(db.Integer, primary_key=True)
    effect_order = db.Column(db.Integer, primary_key=True)
    effect_type = db.Column(db.String(8))
    num_targets = db.Column(db.Integer)

    def __init__(self,action_id,effect_number,effect_type,num_targets=1):
        self.action_id = action_id
        self.effect_order = effect_number
        self.effect_type = effect_type
        self.num_targets = num_targets

    def __repr__(self):
        return '<Effect {1} for Action {0}>'.format(self.action_id,self.effect_number)

class ActionDamage(db.Model):
    action_id = db.Column(db.Integer, db.ForeignKey('action.uid'),
                          primary_key=True)
    effect_order = db.Column(db.Integer,db.ForeignKey('action_effect.effect_order'), primary_key=True)
    damage_type = db.Column(db.String(10))
    power = db.Column(db.Integer)
    element = db.Column(db.String(16))
    split = db.Column(db.Boolean)

    def __init__(self,action_effect,damage_type,power,element="Hidden",split=True):
        self.action_id = action_effect.action_id
        self.effect_order = action_effect.effect_order
        self.damage_type = damage_type
        self.power = power
        self.element = element
        self.split = split

    def __repr__(self):
        return '<Action {0} Damage Effect>'.format(self.action_id)

class ActionStatus(db.Model):
    action_id = db.Column(db.Integer, db.ForeignKey('action.uid'),
                          primary_key=True)
    effect_order = db.Column(db.Integer, db.ForeignKey('action_effect.effect_order'), primary_key=True)
    status = db.Column(db.String(14), primary_key=True)
    mode = db.Column(db.String(8))
    accuracy = db.Column(db.Integer)

    def __init__(self,action_effect,status,mode,accuracy=255):
        self.action_id = action_effect.action_id
        self.effect_order = action_effect.effect_order
        self.status = status
        self.mode = mode
        self.accuracy = accuracy
