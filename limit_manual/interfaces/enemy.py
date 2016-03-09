from flask import render_template, request

from .. import app
from ..relations import enemy as EReln


# Template interface for an enemy
class Enemy(object):
    def __init__(self,name,version=None):
        self.name = name
        self.version = version

        # Find description, image(, and version if not provided)
        base = EReln.EnemyBase.query.filter_by(name=name).one()
        if version == None: version = base.default_version
        self.description = base.description
        self.image = base.image

        # Query for list of all versions of this enemy
        versions = EReln.Enemy.query.filter_by(base=base)

        # Get stats and rewards from table for this specific version
        this_v = versions.filter_by(version=version).one()
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

        self.items = { 'drop': [], 'steal': [], 'morph': None }

        items = EReln.EnemyItem.query.filter_by(enemy=this_v).all()
        for item in items:
            if item.get_method == 'drop':
                self.items['drop'].append( (item.item_name, item.get_chance) )
            elif item.get_method == 'steal':
                self.items['steal'].append( (item.item_name, item.get_chance) )
            else:
                self.items['morph'] = item.item_name

        self.elemental_modifiers = []

        elem_mods = EReln.EnemyElementalModifier.query.filter_by(enemy=this_v).all()
        for mod in elem_mods:
            self.elemental_modifiers.append( { 'element': mod.element, 'modifier': mod.modifier } )

        stat_imms = EReln.EnemyStatusImmunity.query.filter_by(enemy=this_v).all()
        self.status_immunities = { imm.status for imm in stat_imms }

# Route declaration for specific enemy pages
@app.route('/enemies/<name>')
def enemy(name):
    from ..relations.formation import get_formation_ids
    from ..relations.formation import get_formation

    version_name = request.args.get('version', None)

    enemy = Enemy(name,version_name)

    base = EReln.EnemyBase.query.filter_by(name=name).one()
    _all_versions = EReln.Enemy.query.filter_by(base=base)
    _enemy = _all_versions.filter_by(version=enemy.version).one()

    other_versions = { e.version for e in _all_versions.all() if e.version != version_name }

    # Find and arrange all formations containing this enemy
    _formation_ids = get_formation_ids(_enemy)
    formations = [ get_formation(uid) for uid in _formation_ids ]

    return render_template('enemies/enemy.j2',
                           enemy=enemy, other_versions=other_versions,
                           items=enemy.items, elements=enemy.elemental_modifiers, statuses=enemy.status_immunities,
                           formations=formations)
