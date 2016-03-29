from flask import render_template, request

from .. import app, db

# Bare-bones template for a specific enemy sub-type
# Contains a name, image, and description
# Both in comments and in code 'base enemy' will usually mean this
class EnemyBase(db.Model):
    uid = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(200))
    image = db.Column(db.String(50))
    default_version = db.Column(db.String(40))

    def __init__(self, name, description, image, version='Normal'):
        self.name = name
        self.description = description
        self.image = image
        self.default_version = version

    def __repr__(self):
        return '<Base Enemy {0!s}>'.format(self.name)

    def __str__(self):
        return 'Enemy'

# Statted enemy unit, describes a version of an EnemyBase
# Contains all single-value stats and attributes
# Referenced in all of the following classes through enemy and enemy_id
# Both in comments and in code 'enemy' will usually mean this
class Enemy(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey('enemy_base.uid'),
                        nullable=False)
    base = db.relationship('EnemyBase', backref=db.backref('enemy_version', lazy='dynamic'))
    version = db.Column(db.String(40))
    # stats
    level = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    mp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    magic_attack = db.Column(db.Integer)
    magic_defense = db.Column(db.Integer)
    defense_pct = db.Column(db.Integer)
    magic_defense_pct = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    luck = db.Column(db.Integer)
    # rewards
    exp = db.Column(db.Integer)
    ap = db.Column(db.Integer)
    gil = db.Column(db.Integer)

    def __init__(self, base, version,
                 level=7, hp=40, mp=0, attack=12, defense=10,
                 magic_attack=2, magic_defense=2,
                 defense_pct=4, magic_defense_pct=0,
                 dexterity=0, luck=0,
                 exp=22, ap=2, gil=15):
        self.base = base
        self.version = version
        self.level = level
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.magic_attack = magic_attack
        self.magic_defense = magic_defense
        self.defense_pct = defense_pct
        self.magic_defense_pct = magic_defense_pct
        self.dexterity = dexterity
        self.luck = luck
        self.exp = exp
        self.ap = ap
        self.gil = gil

    def __repr__(self):
        return '<Enemy {0!s} ({1!s})>'.format(self.base.name, self.version)

# A relation which tracks an enemy's drops, steals, and morph
# Each instance describes the contents of one of an enemy's item slots
# A maximum of four should exist per enemy, but this is not yet enforced
# Chances are represented as an integer 0 <= chance < 64
class EnemyItem(db.Model):
    enemy_id = db.Column(db.Integer, db.ForeignKey('enemy.uid'),
                         primary_key=True)
    enemy = db.relationship('Enemy',
                            backref=db.backref('item', lazy='dynamic'))
    slot = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(30), nullable=False)
    get_method = db.Column(db.Integer, nullable=False)
    get_chance = db.Column(db.Integer)

    def __init__(self,enemy,slot,item_name,get_method,get_chance=None):
        self.enemy = enemy
        self.slot = slot
        self.item_name = item_name
        self.get_method = get_method
        self.get_chance = get_chance

    def __repr__(self):
        return '<{0!s} from {1!r}>'.format(self.get_method,self.enemy)

# A relation to track an enemy's elemental affinities
# Each instance describes one element's modifiers against one enemy
class EnemyElementalModifier(db.Model):
    enemy_id = db.Column(db.Integer, db.ForeignKey('enemy.uid'),
                         primary_key=True)
    enemy = db.relationship('Enemy',
                            backref=db.backref('elemental_modifier', lazy='dynamic'))
    element = db.Column(db.String(11), primary_key=True)
    modifier = db.Column(db.Integer)

    def __init__(self,enemy,element,modifier):
        self.enemy = enemy
        self.element = element
        self.modifier = modifier

    def __repr__(self):
        return '<{0}:{1}% against {2!r}>'.format(self.element,self.modifier,self.enemy)

# A relation to track an enemy's status immunities
# An instance indicates that enemy is immune to status
class EnemyStatusImmunity(db.Model):
    enemy_id = db.Column(db.Integer, db.ForeignKey('enemy.uid'),
                         primary_key=True)
    enemy = db.relationship('Enemy',
                            backref=db.backref('status_immunity', lazy='dynamic'))
    status = db.Column(db.String(25), primary_key=True)

    def __init__(self,enemy,status):
        self.enemy = enemy
        self.status = status

    def __repr__(self):
        return '<StatusImmunity {0!r}:{1!s}>'.format(self.enemy,self.status)

class EnemyAction(db.Model):
    enemy_id = db.Column(db.Integer, db.ForeignKey('enemy_base.uid'),primary_key=True)
    action = db.Column(db.String(20))
    name_hidden = db.Column(db.Boolean)
    manipulate = db.Column(db.Boolean)
