from flask import render_template, request

from .. import app
from ..relations import enemy as EnemyRelations

class EnemyBase(object):
    @staticmethod
    def db_reference(name):
        return EnemyRelations.EnemyBase.query.filter_by(name=name).one()

    def __init__(self,name):
        self.name = name
        this_enemy = self.db_reference(self.name)
        self.uid = this_enemy.uid

    def all_versions(self):
        db_versions = EnemyRelations.Enemy.query.filter_by(base=self.db_reference(self.name))
        return { v.version for v in db_versions }

# Template interface for an enemy
class Enemy(EnemyBase):
    def __init__(self,name,version=None):
        EnemyBase.__init__(self,name)
        self.version = version

        # Find description, image(, and version if not provided)
        base = EnemyBase.db_reference(self.name)
        if version == None: base.default_version

        self.description = base.description
        self.image = base.image

        # Query for list of all versions of this enemy
        versions = EnemyRelations.Enemy.query.filter_by(base=base)

        # Get stats and rewards from table for this specific version
        this_v = versions.filter_by(version=version).one()
        self.uid = this_v.uid
        self.stats = {
            'level' : this_v.level,
            'hp'    : this_v.hp,
            'mp'    : this_v.mp,
            'attack'    : this_v.attack,
            'defense'   : this_v.defense,
            'magic_attack'  : this_v.magic_attack,
            'magic_defense' : this_v.magic_defense,
            'defense_pct'       : this_v.defense_pct,
            'magic_defense_pct' : this_v.magic_defense_pct,
            'dexterity' : this_v.dexterity,
            'luck'      : this_v.luck
        }
        self.rewards = {
            'exp'   : this_v.exp,
            'ap'    : this_v.ap,
            'gil'   : this_v.gil
        }

        # Find the names of all other versions of this enemy
        self.other_versions = self.all_versions() - { self.version }

        # Fill list of items that can be gotten from this enemy
        self.items = { 'drop': [], 'steal': [], 'morph': None }
        items = EnemyRelations.EnemyItem.query.filter_by(enemy=this_v).all()
        for item in items:
            if item.get_method == 'drop':
                self.items['drop'].append( (item.item_name, item.get_chance) )
            elif item.get_method == 'steal':
                self.items['steal'].append( (item.item_name, item.get_chance) )
            else:
                self.items['morph'] = item.item_name

        self.elemental_modifiers = []
        elem_mods = EnemyRelations.EnemyElementalModifier.query.filter_by(enemy=this_v).all()
        for mod in elem_mods:
            self.elemental_modifiers.append( { 'element': mod.element, 'modifier': mod.modifier } )

        stat_imms = EnemyRelations.EnemyStatusImmunity.query.filter_by(enemy=this_v).all()
        self.status_immunities = { imm.status for imm in stat_imms }

    def get_formations(self):
        from ..relations.formation import get_formation_ids
        from ..relations.formation import get_formation

        formation_ids = get_formation_ids(self.uid)
        return [ get_formation(fid) for fid in formation_ids ]

# Route declaration for specific enemy pages
@app.route('/enemies/<name>')
def enemy(name):
    version_name = request.args.get('version', None)
    enemy = Enemy(name,version_name)

    return render_template('enemies/enemy.j2',
                           enemy=enemy,
                           formations=enemy.get_formations())

@app.route('/enemies')
@app.route('/enemies/all')
def all_enemies():
    from ..relations.formation import get_formation_ids, get_locations

    enemies = []

    for db_base in EnemyRelations.EnemyBase.query.add_columns(EnemyRelations.EnemyBase.uid,EnemyRelations.EnemyBase.name).all():
        info = { 'name': db_base.name }
        info['versions'] = EnemyBase(db_base.name).all_versions()

        enemies.append(info)

    return render_template('enemies/all_enemies.j2', enemies=enemies)
