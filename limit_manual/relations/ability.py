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
    friendly = db.Column(db.Boolean)
    target_all = db.Column(db.Boolean)
    target_random = db.Column(db.Boolean)
    num_attacks = db.Column(db.Integer)
    split = db.Column(db.Boolean)
    has_statuses = db.Column(db.Boolean)
    has_damage = db.Column(db.Boolean)
    has_notes = db.Column(db.Boolean)

    def __init__(self, name, category, description_id=1,
                 hit_formula='Magical', accuracy=256,
                 friendly=False, target_all=False, target_random=True,
                 num_attacks=1, split=True, element='None',
                 has_statuses=False, has_damage=True, has_notes=False):
        self.name = name
        self.category = category
        self.description_id = description_id
        self.hit_formula = hit_formula
        self.element = element
        self.friendly = friendly
        self.target_all = target_all
        self.target_random = target_random
        self.num_attacks = num_attacks
        self.split = split
        self.has_statuses = has_statuses
        self.has_damage = has_damage
        self.has_notes = has_notes

class MagicInfo(db.Model):
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.uid'),
                          primary_key=True)
    mp_cost = db.Column(db.Integer)
    spell_type = db.Column(db.String(8))
    reflectable = db.Column(db.Boolean)

    def __init__(self,ability_id,mp_cost,spell_type='Attack',reflectable=True):
        self.ability_id = ability_id
        self.mp_cost = mp_cost
        self.spell_type = spell_type
        self.reflectable = reflectable

class AbilityDamage(db.Model):
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.uid'),
                          primary_key=True)
    formula = db.Column(db.String(12))
    power = db.Column(db.Integer)
    piercing = db.Column(db.Boolean)

    def __init__(self, ability_id, formula, power, piercing=False):
        self.ability_id = ability_id
        self.formula = formula
        self.power = power
        self.piercing = piercing

class AbilityStatusInfo(db.Model):
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.uid'),
                          primary_key=True)
    mode = db.Column(db.String(8))
    chance = db.Column(db.Integer)

    def __init__(self,ability_id,mode,chance=256):
        self.ability_id = ability_id
        self.mode = mode
        self.chance = chance

class AbilityStatusList(db.Model):
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.uid'),
                          primary_key=True)
    status = db.Column(db.String(25), primary_key=True)

    def __init__(self,ability_id,status):
        self.ability_id = ability_id
        self.status = status

class AbilityNotes(db.Model):
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.uid'),
                           primary_key=True)
    note_id = db.Column(db.Integer, primary_key=True)
    note_text = db.Column(db.String(80))

    def __init__(self,ability_id,note_id,note_text):
        self.ability_id = ability_id
        self.note_id = note_id
        self.note_text = note_text
