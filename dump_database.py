import json

def formatted_json_dump(data):
    return json.dumps( data, indent=2, separators=(',',': ') )

with open('data_backups/enemies.json','w') as f:
    from limit_manual.interfaces.enemy import EnemyBase
    all_enemies = EnemyBase.extract_all(with_uid=True)
    print(f.write( formatted_json_dump(all_enemies) ))

with open('data_backups/characters.json','w') as f:
    from limit_manual.interfaces.character import Character
    all_characters = Character.extract_all(with_uid=True)
    print(f.write( formatted_json_dump(all_characters) ))

with open('data_backups/items.json','w') as f:
    from limit_manual.interfaces.item import Item
    all_items = Item.extract_all(with_uid=True)
    print(f.write( formatted_json_dump(all_items) ))
