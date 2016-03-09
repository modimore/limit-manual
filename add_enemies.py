import json
from limit_manual.enemy import (db, EnemyBase, Enemy, EnemyItem,
                                EnemyStatusImmunity, EnemyElementalModifier)

# add an individual enemy to the database
def add_enemy(enemy):
    if len(EnemyBase.query.filter_by(name=enemy['name']).all()) == 0:
        base = EnemyBase(enemy['name'],enemy['description'],enemy['image'],enemy['default_version'])
        db.session.add(base)
    else:
        base = EnemyBase.query.filter_by(name=enemy['name']).one()

    for version in enemy['versions']:
        if len(Enemy.query.filter_by(base=base).filter_by(version=version['version']).all()) != 0:
            continue

        enemy = Enemy(base,version['version'],**version['info'])
        db.session.add(enemy)

        for i in range(len(version['items'])):
            db.session.add(EnemyItem(enemy,i,**version['items'][i]))

        for status in version['status_immunities']:
            db.session.add(EnemyStatusImmunity(enemy,status))

        for modifier in version['elemental_modifiers']:
            db.session.add(EnemyElementalModifier(enemy,**modifier))

    db.session.commit()

def upload_from_json(filename="testing/enemy_data.json"):
    document = json.load(open(filename,'r'))

    for enemy in document:
        add_enemy(enemy)

if __name__ == '__main__':
    upload_from_json()
