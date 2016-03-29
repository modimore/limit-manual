from flask import render_template

from .. import app
from ..relations import action as AbilityRelations
from ..relations.miscellaneous import get_description

class Ability(object):
    @staticmethod
    def db_reference(name):
        return AbilityRelations.Ability.query.filter_by(name=name).one_or_none()

    def __init__(self,name):
        self.name = name
        db_ref = Ability.db_reference(self.name)
        self.uid = db_ref.uid
        self.category = db_ref.category
        self.hit_formula = db_ref.hit_formula
        self.element = db_ref.element

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

        if new_action.num_statuses > 0:
            for status in act_in['statuses']['list']:
                db.session.add(AbilityRelations.AbilityStatus(act_id,status,act_in['statuses']['mode'],act_in['statuses']['accuracy']))

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

@app.route('/actions')
@app.route('/actions/all')
def all_actions():
    abilities = [ Ability(a.name) for a in AbilityRelations.Ability.query.all() ]
    return render_template('actions/all_actions.j2',
                           abilities=abilities)
