from limit_manual import db
from limit_manual.enemy import EnemyBase, Enemy
from limit_manual.formation import FormationLocation, FormationEnemy

class Enemy2(object):
    def __init__(self,name,version,position):
        self.name = name.strip()
        self.version = version.strip()
        self.position = position

    def get_db_reference(self):
        base = EnemyBase.query.filter_by(name=self.name).one()
        return Enemy.query.filter_by(base=base).filter_by(version=self.version).one()

class Location(object):
    def __init__(self,name,areas):
        self.name = name.strip()
        self.areas = [area.strip() for area in areas]

    def __repr__(self):
        return '<{}>'.format(self.name)

class FullFormation(object):
    def __init__(self,locations,rows):
        self.id = len({ entry.formation_id for entry in FormationLocation.query.all() })
        self.locations = locations
        self.rows = rows

    def __repr__(self):
        return '<Formation {0}>'.format(self.id)

    def commit(self):
        for location in self.locations:
            for area in location.areas:
                db.session.add(FormationLocation(self.id,location.name,area))

        for row in self.rows:
            for enemy in row[1]:
                db.session.add(FormationEnemy(self.id,row[0],enemy.position,enemy.get_db_reference()))

        db.session.commit()

if __name__ == '__main__':
    f = open('testing/formation_data.txt', 'r')
    if f.readline().strip() != '-start':
        import sys
        sys.exit(0)
    locations = []
    rows = []
    for line in f:
        command = line.strip().split(':')
        if command[0] == 'location':
            areas = command[2].split(',')
            locations.append(Location(command[1],areas))
        elif command[0] == 'row':
            row = []
            for enemy in command[2].split(','):
                enemy = enemy.split('#')
                row.append(Enemy2(enemy[0],enemy[1],len(row)))
            rows.append((int(command[1]),row))
        elif command[0] == '-commit':
            formation = FullFormation(locations,rows)
            formation.commit()
            locations = []
            rows = []
