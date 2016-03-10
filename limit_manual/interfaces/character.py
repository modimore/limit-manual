from flask import render_template

from limit_manual import app, db

class Character(object):
    @staticmethod
    def db_reference(name):
        pass

    def __init__(self,name):
        self.name = name

@app.route('/characters')
@app.route('/characters/all')
def all_characters():
    names = ['Cloud','Barret','Tifa','Aeris']
    characters = [ Character(name) for name in names ]

    return render_template('characters/all_characters.j2',
                           characters=characters)
