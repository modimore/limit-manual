from flask import render_template, request

from limit_manual import app, db
from limit_manual.enemy import EnemyBase, Enemy

# A relation to track enemy formations
# Each instance associates an enemy with a row and a position in that row
class FormationEnemy(db.Model):
    formation_id = db.Column(db.Integer, primary_key=True)
    row_num = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, primary_key=True)
    enemy_id = db.Column(db.Integer, db.ForeignKey('enemy.uid'))
    enemy = db.relationship('Enemy',
                            backref=db.backref('formation', lazy='dynamic'))

    def __init__(self,formation_id,row_num,position,enemy):
        self.formation_id = formation_id
        self.row_num = row_num
        self.position = position
        self.enemy = enemy

    def __repr__(self):
        return '<{0!r} in Formation {1}>'.format(self.enemy,self.formation_id)

# A relation to track formation locations
class FormationLocation(db.Model):
    formation_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(40), primary_key=True)
    area = db.Column(db.String(40), primary_key=True)

    def __init__(self, formation_id, location, area):
        self.formation_id = formation_id
        self.location = location
        self.area = area

    def __repr__(self):
        return '<Formation {0} in {1}>'.format(self.formation_id,self.location)

def get_formation_ids(enemy):
    _formations = FormationEnemy.query.filter_by(enemy=enemy).all()
    formation_ids = { f.formation_id for f in _formations }
    return formation_ids

def get_formation(uid):
    formation = {
        'id': uid,
        'locations': [],
        'enemy_rows': []
    }

    _locations = FormationLocation.query.filter_by(formation_id=uid)
    for location in { _loc.location for _loc in _locations.all() }:
        areas = { _loc.area for _loc in _locations.filter_by(location=location).all() }
        formation['locations'].append({ 'name': location, 'areas': areas })

    _enemies = FormationEnemy.query.filter_by(formation_id=uid)
    for row_num in { _e.row_num for _e in _enemies.all() }:
        enemies = [ {'name': _e.enemy.base.name, 'version': _e.enemy.version } for _e in _enemies.filter_by(row_num=row_num).all() ]
        formation['enemy_rows'].append({ 'row_num': row_num, 'enemies': enemies })

    return formation
