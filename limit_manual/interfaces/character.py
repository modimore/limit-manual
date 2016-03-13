from flask import render_template

from limit_manual import app, db
from limit_manual.relations import character as CharacterRelations

class Character(object):
    @staticmethod
    def db_reference(name):
        return CharacterRelations.Character.query.filter_by(name=name).one_or_none()

    def __init__(self,name):
        self.name = name
        db_ref = Character.db_reference(self.name)
        self.uid = db_ref.uid
        self.main_image = 'images/characters/{0}.png'.format('cloud-intro')

    def get_intro(self):
        db_intro = CharacterRelations.CharacterIntro.query.filter_by(uid=self.uid).one_or_none()
        if (db_intro == None): return None

        return {
            'full_name' : db_intro.full_name,
            'job'   : db_intro.job,
            'age'   : db_intro.age,
            'weapon': db_intro.weapon,
            'height': db_intro.height,
            'birthdate' : db_intro.birthdate,
            'birthplace': db_intro.birthplace,
            'blood_type': db_intro.blood_type,
            'description': db_intro.description
        }

@app.route('/characters')
@app.route('/characters/all')
def all_characters():
    names = ['Cloud','Barret','Tifa','Aeris']
    characters = [ Character(c.name) for c in CharacterRelations.Character.query.all() ]

    return render_template('characters/all_characters.j2',
                           characters=characters)

@app.route('/characters/<name>')
def character(name):
    character = Character(name)

    return render_template('characters/character.j2',
                           character=character,
                           intro=character.get_intro())
