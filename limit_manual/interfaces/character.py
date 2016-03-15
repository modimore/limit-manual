from flask import render_template

from .. import app, db
from ..relations import character as CharacterRelations

class Character(object):
    @staticmethod
    def db_reference(name):
        return CharacterRelations.Character.query.filter_by(name=name).one_or_none()

    def __init__(self,name):
        self.name = name
        db_ref = Character.db_reference(self.name)
        self.uid = db_ref.uid
        self.main_image = 'images/characters/{0}-intro.png'.format(name.lower().replace(' ','_'))

    def get_intro(self):
        db_intro = CharacterRelations.CharacterIntro.query.filter_by(uid=self.uid).one_or_none()
        if (db_intro == None): return None

        if db_intro.birthdate.find('/') == -1:
            date_string = 'unknown'
        else:
            month, day = (int(x) for x in db_intro.birthdate.split('/'))
            months = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]
            date_string = '{0} {1}'.format(months[month-1],day)

        height_string = '{0}\''.format(db_intro.height//12) + ('{0}\"'.format(db_intro.height%12) if db_intro.height%12 != 0 else '')

        return {
            'full_name' : db_intro.full_name,
            'job'   : db_intro.job,
            'age'   : db_intro.age if db_intro.age != 0 else "unknown",
            'weapon': db_intro.weapon,
            'height': height_string,
            'birthdate' : date_string,
            'birthplace': db_intro.birthplace if db_intro.birthplace != "" else "unknown",
            'blood_type': db_intro.blood_type if db_intro.blood_type != "" else "unknown",
            'description': db_intro.description
        }

    def extract(self, with_uid=False):
        result = {
            'name': self.name,
            'intro': self.get_intro()
        }

        if with_uid: result['uid'] = self.uid

        return result

    @staticmethod
    def extract_all(with_uid=False):
        all_characters = []
        for c in CharacterRelations.Character.query.all():
            all_characters.append( Character(c.name).extract(with_uid) )
        return all_characters


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
