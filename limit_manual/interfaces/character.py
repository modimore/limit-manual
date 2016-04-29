from flask import render_template

from .. import app, get_connection

class Character(object):
    def __init__(self,name):
        self.name = name
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT uid FROM character;")
            row = c.fetchone()
            self.uid = row[0]
            self.main_image = 'images/characters/{0}-intro.png'.format(name.lower().replace(' ','_'))

            c.execute("SELECT * FROM character_intro WHERE uid=?",(self.uid,))
            row = c.fetchone()

            if row == None:
                self.intro = None
            else:
                month, day = (int(x) for x in row[6].split('/'))
                months = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]
                date_string = '{0} {1}'.format(months[month-1],day)

                self.intro = {
                    'full_name' : row[1],
                    'job'   : row[2],
                    'age'   : row[3] if row[3] != 0 else "unknown",
                    'weapon': row[4],
                    'height': row[5],
                    'birthdate' : date_string,
                    'birthplace': row[7] if row[7] != "" else "unknown",
                    'blood_type': row[8] if row[8] != "" else "unknown",
                    'description': row[9]
                }

    def extract(self, with_uid=False):
        result = {
            'name': self.name,
            'intro': self.intro
        }

        if with_uid: result['uid'] = self.uid

        return result

    @staticmethod
    def extract_all(with_uid=False):
        all_characters = []

        conn = get_connection()
        c = conn.cursor()
        cnames = [ r[0] for r in c.execute("SELECT name FROM character;").fetchall() ]
        conn.close()

        for name in cnames:
            all_characters.append( Character(name).extract(with_uid) )

        return all_characters


@app.route('/characters')
@app.route('/characters/all')
def all_characters():
    characters = []
    conn = get_connection()
    c = conn.cursor()
    cnames = [ r[0] for r in c.execute("SELECT name FROM character WHERE name != 'Sephiroth';").fetchall() ]
    characters = [ {"name": name, "image": "{0}-field.png".format(name.lower().replace(" ","_")) } for name in cnames ]
    conn.close()

    return render_template('characters/all_characters.j2',
                           characters=characters)

@app.route('/characters/<name>')
def character(name):
    return render_template('characters/character.j2',
                           character=Character(name))
