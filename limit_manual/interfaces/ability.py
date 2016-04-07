from flask import render_template, request

from .. import app
from ..relations import ability as AbilityRelations
from ..relations.miscellaneous import get_description, add_description

class Ability(object):
    @staticmethod
    def db_reference(name=None,uid=None):
        if uid != None:
            return AbilityRelations.Ability.query.filter_by(uid=uid).one_or_none()
        elif name != None:
            return AbilityRelations.Ability.query.filter_by(name=name).one_or_none()
        else:
            return None

    def get_statuses(self):
        info = AbilityRelations.AbilityStatusInfo.query.filter_by(ability_id=self.uid).one()
        status_list = [ r.status for r in AbilityRelations.AbilityStatusList.query.filter_by(ability_id=self.uid).all() ]

        self.statuses = {
            'list': status_list,
            'mode': info.mode,
            'chance': info.chance
        }

    def get_damage(self):
        damage = AbilityRelations.AbilityDamage.query.filter_by(ability_id=self.uid).one()

        self.damage = {
            'formula': damage.formula,
            'power': damage.power,
            'piercing': damage.piercing,
            'physical': damage.formula == 'Physical'
        }

        self.get_damage_string()

    def get_damage_string(self):
        if self.damage['formula'] == 'Max HP%':
            if self.damage['power'] == 32:
                self.damage_text = 'Restore HP to full'
            else:
                self.damage_text = 'Heal damage equal to {0}% of Max HP'.format(100*self.damage['power']//32)
        elif self.damage['formula'] == 'Cure':
            if self.damage['power'] < 20: level = 'light'
            elif self.damage['power'] < 40: level = 'moderate'
            else: level = 'major'

            self.damage_text = 'Heal a {0} amount of damage'.format(level)
        elif self.damage['formula'] == 'HP%':
            self.damage_text = 'Deal damage equal to {0}% of target\'s current HP'.format(100*self.damage['power']//32)
        else:
            damage_properties = []
            if self.damage['power'] < 20: damage_properties.append('light')
            elif self.damage['power'] < 40: damage_properties.append('moderate')
            elif self.damage['power'] < 80: damage_properties.append('high')
            else: damage_properties.append('heavy')

            if self.element != 'None':
                damage_properties.append('{0}-elemental'.format(self.element))

            self.damage_text = 'Deals {0} damage'.format(' '.join(damage_properties).lower())

            if self.target_all or self.num_attacks > 1:
                self.damage_text = self.damage_text + ' to each target'

    def __init__(self,name=None,uid=None):
        base_ref = Ability.db_reference(name=name,uid=uid)
        # common attributes of all abilities
        self.name = base_ref.name
        self.uid = base_ref.uid
        self.category = base_ref.category

        ability_notes = []
        if base_ref.has_notes:
            for _note in AbilityRelations.AbilityNotes.query.filter_by(ability_id=self.uid).all():
                ability_notes.append(_note.note_text)

        if base_ref.has_info:
            info_ref = AbilityRelations.AbilityInfo.query.filter_by(uid=self.uid).one()
            self.hit_formula = info_ref.hit_formula
            self.accuracy = info_ref.accuracy
            self.element = info_ref.element
            self.friendly = info_ref.friendly
            self.target_all = info_ref.target_all
            self.target_random = info_ref.target_random
            self.num_attacks = info_ref.num_attacks
            self.split = info_ref.split

            if info_ref.has_statuses:
                self.get_statuses()
            else: self.statuses = None

            if info_ref.has_damage:
                self.get_damage()
            else: self.damage = None

            if self.target_all:
                ability_notes.append('targets entire party')
            elif self.target_random:
                if self.num_attacks == 1:
                    ability_notes.append('selects one target randomly')
                else:
                    ability_notes.append('selects a random target {0} times'.format(self.num_attacks))

            if self.split == False:
                ability_notes.append('full power multi-target')

        if len(ability_notes) > 0:
            self.notes_string = ', '.join(ability_notes)
        else:
            self.notes_string = None

        self.in_game_description = get_description(base_ref.description_id,"Ability",self.uid)

    @staticmethod
    def create(act_in):
        from .. import db
        new_action = AbilityRelations.Ability(act_in['name'],act_in['category'],has_info=('info' in act_in.keys()),has_notes=('notes' in act_in.keys()))
        db.session.add(new_action)
        db.session.commit()
        act_id = new_action.uid

        if 'notes' in act_in.keys():
            for i in range(len(act_in['notes'])):
                db.session.add(AbilityRelations.AbilityNotes(act_id,i,act_in['notes'][i]))

        if 'info' in act_in.keys():
            db.session.add(AbilityRelations.AbilityInfo(act_id,**act_in['info']))

        if new_action.category == "Magic":
            db.session.add(AbilityRelations.MagicInfo(act_id,**act_in['magic_info']))
        elif new_action.category == "Summon":
            db.session.add(AbilityRelations.SummonInfo(act_id,act_in['summon_info']['mp_cost'],len(act_in['summon_info']['attacks'])))
            for attack in act_in['summon_info']['attacks']:
                Ability.create(attack)
                attack_id = Ability(attack['name']).uid
                db.session.add(AbilityRelations.SummonAttacks(act_id,attack_id))
                db.session.commit()

        if 'description' in act_in:
            new_action.descr_id = add_description('Ability',act_id,**act_in['description'])


        if 'statuses' in act_in.keys():
            db.session.add(AbilityRelations.AbilityStatusInfo(act_id,**act_in['statuses']['info']))
            for status in act_in['statuses']['list']:
                db.session.add(AbilityRelations.AbilityStatusList(act_id,status))

        if 'damage' in act_in.keys():
            db.session.add(AbilityRelations.AbilityDamage(act_id,**act_in['damage']))

        db.session.commit()

class Spell(Ability):
    def get_magic_info(self):
        return AbilityRelations.MagicInfo.query.filter_by(ability_id=self.uid).one()

    def __init__(self,name):
        Ability.__init__(self,name)

        magic_info = self.get_magic_info()
        self.mp_cost = magic_info.mp_cost
        self.spell_type = magic_info.spell_type
        self.reflectable = magic_info.reflectable

class Summon(Ability):
    def get_summon_info(self):
        return AbilityRelations.SummonInfo.query.filter_by(ability_id=self.uid).one()

    def get_attacks(self):
        attack_ids = [ row.attack_id for row in AbilityRelations.SummonAttacks.query.filter_by(summon_id=self.uid).all() ]

        return [ Ability(uid=a_id) for a_id in attack_ids ]


    def __init__(self,name):
        Ability.__init__(self,name)

        summon_info = self.get_summon_info()

        self.mp_cost = summon_info.mp_cost
        self.attacks = self.get_attacks()


@app.route('/abilities')
@app.route('/abilities/all')
def all_actions():
    _abilities = AbilityRelations.Ability.query.all()

    spells = []
    summons = []

    for ability in _abilities:
        if ability.category == "Magic":
            spells.append(Spell(ability.name))
        elif ability.category == "Summon":
            summons.append(Summon(ability.name))

    spell_content = render_template('abilities/magic/simple_spells.j2',
                                    spells=spells)
    summon_content = render_template('abilities/summons/simple_summons.j2',
                                     summons=summons)

    return render_template('abilities/all_abilities.j2',
                           spell_content=spell_content,
                           summon_content=summon_content)

@app.route('/abilities/magic')
@app.route('/abilities/spells')
def all_magic():
    detail = (request.args.get('display',None) in ['Detail','detail'])

    _spells = AbilityRelations.Ability.query.filter_by(category='Magic').all()

    restore = []
    attack = []
    indirect = []
    other = []

    for _spell in _spells:
        spell = Spell(_spell.name)
        if spell.spell_type == "Restore":
            restore.append(spell)
        elif spell.spell_type == "Attack":
            attack.append(spell)
        elif spell.spell_type == "Indirect":
            indirect.append(spell)
        else:
            other.append(spell)

    return render_template('abilities/magic/magic.j2', detail=detail,
                           restore=restore, attack=attack,
                           indirect=indirect, other=other)

@app.route('/abilities/summons')
def all_summons():
    _summons = AbilityRelations.Ability.query.filter_by(category='Summon').all()

    summons = [ Summon(_summon.name) for _summon in _summons ]

    return render_template('abilities/summons/summons.j2',
                           summons=summons)
