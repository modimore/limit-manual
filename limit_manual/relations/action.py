from .. import db
from .miscellaneous import DescriptionFormat

class Ability(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description_id = db.Column(db.Integer,
                               db.ForeignKey('description_format.uid'))
    category = db.Column(db.String(20))
    hit_formula = db.Column(db.String(8))
    accuracy = db.Column(db.Integer)
    element = db.Column(db.String(16))
    default_target_group = db.Column(db.String(8))
    num_targets = db.Column(db.Integer)
    split = db.Column(db.Boolean)
    num_statuses = db.Column(db.Integer)
    has_damage = db.Column(db.Boolean)

    def __init__(self, name, category, description_id=1,
                 hit_formula='Magical', accuracy=255,
                 default_target_group='Enemies', num_targets=1, split=True,
                 element='', num_statuses=0, has_damage=True):
        self.name = name
        self.category = category
        self.description_id = description_id
        self.hit_formula = hit_formula
        self.element = element
        self.default_target_group = default_target_group
        self.num_targets = num_targets
        self.split = split
        self.num_statuses = num_statuses
        self.has_damage = has_damage

class MagicInfo(db.Model):
    action_id = db.Column(db.Integer, db.ForeignKey('ability.uid'),
                          primary_key=True)
    mp_cost = db.Column(db.Integer)
    spell_type = db.Column(db.String(8))
    reflectable = db.Column(db.Boolean)

    def __init__(self,action_id,mp_cost,spell_type='Attack',reflectable=True):
        self.action_id = action_id
        self.mp_cost = mp_cost
        self.spell_type = spell_type
        self.reflectable = reflectable

class AbilityDamage(db.Model):
    action_id = db.Column(db.Integer, db.ForeignKey('ability.uid'),
                          primary_key=True)
    formula = db.Column(db.String(12))
    power = db.Column(db.Integer)
    piercing = db.Column(db.Boolean)

    def __init__(self, action_id, formula, power, piercing=False):
        self.action_id = action_id
        self.formula = formula
        self.power = power
        self.piercing = piercing

class AbilityStatus(db.Model):
    action_id = db.Column(db.Integer, db.ForeignKey('ability.uid'),
                          primary_key=True)
    status = db.Column(db.String(25), primary_key=True)
    mode = db.Column(db.String(8))
    accuracy = db.Column(db.Integer)

    def __init__(self,action_id,status,mode="Grant",accuracy=255):
        self.action_id = action_id
        self.status = status
        self.mode = mode
        self.accuracy = accuracy
