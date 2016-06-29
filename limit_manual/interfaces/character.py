from flask import render_template

from .. import app, get_connection

class Character(object):
    def __init__(self,name):
        self.name = name
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT uid FROM characters WHERE name=%s", (self.name,))
            row = c.fetchone()
            self.uid = row[0]
            self.main_image = 'images/characters/{0}-intro.png'.format(name.lower().replace(' ','_'))

            c.execute('''SELECT full_name, job, age, weapon, height,
                                birthdate, birthplace, blood_type, description
                         FROM character_intros
                         WHERE uid=%s''', (self.uid,))
            row = c.fetchone()

            if row == None:
                self.intro = None
            else:
                try:
                    month, day = (int(x) for x in row[5].split('/'))
                    months = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]
                    date_string = '{0} {1}'.format(months[month-1],day)
                except ValueError:
                    date_string = row[5]

                self.intro = {
                    'full_name' : row[0],
                    'job'   : row[1],
                    'age'   : row[2] if row[2] != 0 else "unknown",
                    'weapon': row[3],
                    'height': row[4],
                    'birthdate' : date_string if date_string != "" else "unknown",
                    'birthplace': row[6] if row[6] != "" else "unknown",
                    'blood_type': row[7] if row[7] != "" else "unknown",
                    'description': row[8]
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
        cnames = [ r[0] for r in c.execute("SELECT name FROM characters;").fetchall() ]
        conn.close()

        for name in cnames:
            all_characters.append( Character(name).extract(with_uid) )

        return all_characters


@app.route('/characters')
@app.route('/characters/all')
def all_characters():
    ''' Generate page to list all characters. '''
    characters = []
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM characters WHERE name != 'Sephiroth'")
    cnames = [ r[0] for r in cur.fetchall()]
    characters = [ {"name": name, "image": "{0}-field.png".format(name.lower().replace(" ","_")) } for name in cnames ]
    conn.close()

    return render_template('characters/all_characters.j2',
                           characters=characters)

@app.route('/characters/<name>')
def character(name):
    ''' Generate page with information on a specific character '''
    return render_template('characters/character.j2',
                           character=Character(name))
