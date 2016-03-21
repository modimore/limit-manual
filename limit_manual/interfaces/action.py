from flask import render_template

from .. import app
from ..relations import action as ActionRelations

class Action(object):
    @staticmethod
    def db_reference(name):
        return ActionRelations.Action.query.filter_by(name=name).one_or_none()

    def __init__(self,name):
        self.name = name
        db_ref = Action.db_reference(self.name)
        self.uid = db_ref.uid
        self.category = db_ref.category

        self.get_damage()
        self.get_properties()

    def get_damage(self):
        damage_rows = ActionRelations.ActionDamage.query.filter_by(action_id=self.uid).all()
        if len(damage_rows) == 0:
            self.primary_damage = None
            self.secondary_damage = None
        elif (len(damage_rows) == 1):
            self.primary_damage = { 'modifier': damage_rows[0].modifier, 'element': damage_rows[0].element, 'split': damage_rows[0].split }
            self.secondary_damage = None
        else:
            for damage in damage_rows:
                if damage.primary == True:
                    self.primary_damage = { 'modifier': damage.modifier, 'element': damage.element, 'split': damage.split }
                else:
                    self.secondary_damage = { 'modifier': damage.modifier, 'element': damage.element, 'split': damage.split }

    def get_properties(self):
        properties_r = ActionRelations.ActionProperty.query.filter_by(action_id=self.uid).all()
        return { p.description: p.value for p in properties_r }

    @staticmethod
    def create(actionspec):
        from .. import db
        action_r = {
            'name': actionspec['name'],
            'category': actionspec['category']
        }
        new_action = ActionRelations.Action(**action_r)
        db.session.add(new_action)
        db.session.commit()
        act_id = new_action.uid

        if 'damage' in actionspec.keys():
            db.session.add(ActionRelations.ActionDamage(new_action.uid,**actionspec['damage']))

            if 'secondary_damage' in actionspec.keys():
                db.session.add(ActionRelations.ActionDamage(act_id,primary=False,**actionspec['secondary_damage']))

        if 'properties' in actionspec.keys():
            for i in range(len(actionspec['properties'])):
                p = actionspec['properties'][i]
                db.session.add(ActionRelations.ActionProperty(act_id,i+1,*p))

        db.session.commit()


    def extract(self, with_uid=False):
        result = {
            'name': self.name,
            'category': self.category
        }

        if with_uid: result['uid'] = self.uid

        return result

    @staticmethod
    def extract_all(with_uid=False):
        actions = []
        for a in ActionRelations.Action.query.all():
            actions.append( Action(a.name).extract(with_uid) )
        return actions

@app.route('/actions')
@app.route('/actions/all')
def all_actions():
    actions = [ Action(a.name) for a in ActionRelations.Action.query.all() ]
    return render_template('actions/all_actions.j2',
                           actions=actions)
