import json
from limit_manual.enemy import (db, EnemyBase, Enemy, EnemyItem,
                                EnemyStatusImmunity, EnemyElementalModifier)

# add an individual enemy to the database
def add_enemy(enemy):
    base = EnemyBase(enemy['name'],enemy['description'],enemy['image'])
    db.session.add(base)

    for version in enemy['versions']:
        enemy = Enemy(base,version['version'],**version['info'])
        db.session.add(enemy)

        for i in range(len(version['items'])):
            db.session.add(EnemyItem(enemy,i,**version['items'][i]))

        for status in version['status_immunities']:
            db.session.add(EnemyStatusImmunity(enemy,status))

        for modifier in version['elemental_modifiers']:
            db.session.add(EnemyElementalModifier(enemy,**modifier))

    db.session.commit()

def upload_from_json(filename="enemy_data.json"):
    document = json.load(open(filename,'r'))

    for enemy in document:
        add_enemy(enemy)

if __name__ == '__main__':
    upload_from_json()
