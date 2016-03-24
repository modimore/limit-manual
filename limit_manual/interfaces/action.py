from flask import render_template

from .. import app
from ..relations import action as ActionRelations
from ..relations.miscellaneous import get_description

class Action(object):
    @staticmethod
    def db_reference(name):
        return ActionRelations.Action.query.filter_by(name=name).one_or_none()

    def get_spell_properties(self):
        spell_info_r = ActionRelations.SpellInfo.query.filter_by(action_id=self.uid).one()
        self.spell_info = {
            'mp_cost': spell_info_r.mp_cost,
            'reflectable': spell_info_r.reflectable
        }

    def get_effects(self):
        result = []

        ordered_effects = ActionRelations.ActionEffect.query.filter_by(action_id=self.uid).order_by(ActionRelations.ActionEffect.effect_order.desc()).all()

        for effect in ordered_effects:
            if effect.effect_type == "damage":
                damage_row = ActionRelations.ActionDamage.query.filter_by(action_id=self.uid).filter_by(effect_order=effect.effect_order).one()
                result.append({
                    'type': 'damage',
                    'num_targets': effect.num_targets,
                    'info': {
                        'damage_type': damage_row.damage_type,
                        'power': damage_row.power,
                        'element': damage_row.element,
                        'split': damage_row.split
                    }
                })
            elif effect.effect_type == "status":
                status_rows = ActionRelations.ActionStatus.query.filter_by(action_id=self.uid).filter_by(effect_order=effect.effect_order).all()
                this_status = {
                    'type': 'status',
                    'statuses': [ row.status for row in status_rows ],
                    'num_targets': effect.num_targets,
                    'info': {
                        'mode': status_rows[0].mode,
                        'accuracy': status_rows[0].accuracy
                    }
                }
                result.append(this_status)

        self.effects = result

    def __init__(self,name):
        self.name = name
        db_ref = Action.db_reference(self.name)
        self.uid = db_ref.uid
        self.category = db_ref.category

        if self.category in ["Spell", "Summon", "Enemy Skill"]:
            self.get_spell_properties()

        self.get_effects()

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

        if new_action.category in [ "Spell", "Enemy Skill", "Summon" ]:
            db.session.add(ActionRelations.SpellInfo(act_id,**actionspec['spell_info']))

        for i in range(len(actionspec['effects'])):
            effect = actionspec['effects'][i]
            if 'num_targets' in effect:
                effect_row = ActionRelations.ActionEffect(act_id,i,effect['type'],effect['num_targets'])
            else:
                effect_row = ActionRelations.ActionEffect(act_id,i,effect['type'])
            db.session.add(effect_row)

            if (effect['type'] == 'damage'):
                db.session.add(ActionRelations.ActionDamage(effect_row, **effect['info']))
            elif (effect['type'] == 'status'):
                for status in effect['statuses']:
                    db.session.add(ActionRelations.ActionStatus(effect_row, status, **effect['info']))

        db.session.commit()


    def extract(self, with_uid=False):
        result = {
            'name': self.name,
            'category': self.category,
            'effects': self.effects
        }

        if self.category in [ "Spell", "Summon", "Enemy Skill" ]:
            result['spell_info'] = self.spell_info

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
