from flask import render_template

from .. import app
from ..relations import action as AbilityRelations
from ..relations.miscellaneous import get_description

class Ability(object):
    @staticmethod
    def db_reference(name):
        return AbilityRelations.Ability.query.filter_by(name=name).one_or_none()

    def get_statuses(self):
        print(self.name)
        info = AbilityRelations.AbilityStatusInfo.query.filter_by(action_id=self.uid).one()
        status_list = [ r.status for r in AbilityRelations.AbilityStatusList.query.filter_by(action_id=self.uid).all() ]

        self.statuses = {
            'list': status_list,
            'mode': info.mode,
            'chance': info.chance
        }

    def get_damage(self):
        damage = AbilityRelations.AbilityDamage.query.filter_by(action_id=self.uid).one()

        self.damage = {
            'formula': damage.formula,
            'power': damage.power,
            'piercing': damage.piercing,
            'physical': damage.formula == 'Physical'
        }

    def __init__(self,name):
        self.name = name
        db_ref = Ability.db_reference(self.name)
        # common attributes of all abilities
        self.uid = db_ref.uid
        self.category = db_ref.category
        self.hit_formula = db_ref.hit_formula
        self.accuracy = db_ref.accuracy
        self.element = db_ref.element
        self.default_target_group = db_ref.default_target_group
        self.num_targets = db_ref.num_targets
        self.split = db_ref.split

        if db_ref.has_statuses:
            self.get_statuses()
        else: self.statuses = None

        if db_ref.has_damage:
            self.get_damage()
        else: self.damage = None

        self.description = get_description(db_ref.description_id,"Ability",self.uid)

    @staticmethod
    def create(act_in):
        from .. import db
        new_action = AbilityRelations.Ability(act_in['name'],act_in['category'],**act_in['basic_info'])
        db.session.add(new_action)
        db.session.commit()
        act_id = new_action.uid

        if new_action.category == "Magic":
            db.session.add(AbilityRelations.MagicInfo(act_id,**act_in['magic_info']))

        if new_action.has_statuses:
            db.session.add(AbilityRelations.AbilityStatusInfo(act_id,act_in['statuses']['mode'],act_in['statuses']['accuracy']))
            for status in act_in['statuses']['list']:
                db.session.add(AbilityRelations.AbilityStatusList(act_id,status))

        if new_action.has_damage:
            db.session.add(AbilityRelations.AbilityDamage(act_id,**act_in['damage']))

        db.session.commit()


    def extract(self, with_uid=False):
        basic_info = {
            'hit_formula': self.hit_formula,
            'element': self.element
        }

        result = {
            'name': self.name,
            'category': self.category,
            'basic_info': basic_info
        }

        if with_uid: result['uid'] = self.uid

        return result

    @staticmethod
    def extract_all(with_uid=False):
        actions = []
        for a in AbilityRelations.Action.query.all():
            actions.append( Action(a.name).extract(with_uid) )
        return actions

class Spell(Ability):
    def get_magic_info(self):
        return AbilityRelations.MagicInfo.query.filter_by(action_id=self.uid).one()

    def __init__(self,name):
        Ability.__init__(self,name)

        magic_info = self.get_magic_info()
        self.mp_cost = magic_info.mp_cost
        self.spell_type = magic_info.spell_type
        self.reflectable = magic_info.reflectable

@app.route('/actions')
@app.route('/actions/all')
def all_actions():
    _abilities = AbilityRelations.Ability.query.all()

    spells = []

    for ability in _abilities:
        if ability.category == "Magic":
            spells.append(Spell(ability.name))

    return render_template('actions/all_actions.j2',
                           spells=spells)
