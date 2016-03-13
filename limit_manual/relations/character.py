# This file is nowhere near functional, but I know I will need it in the future
# The relations to represent this information have not been worked out yet

from flask import render_template

from .. import app, db

class Character(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Character {0!s}>'.format(self.name)

class CharacterIntro(db.Model):
    uid = db.Column(db.Integer, db.ForeignKey('character.uid'),
                    primary_key=True)
    full_name = db.Column(db.String(18))
    job = db.Column(db.String(33))
    age = db.Column(db.Integer)
    weapon = db.Column(db.String(40))
    height = db.Column(db.Integer)
    birthdate = db.Column(db.String(5))
    birthplace = db.Column(db.String(13))
    blood_type = db.Column(db.String(2))
    description = db.Column(db.String(365))

    def __init__(self,uid,full_name,job,age,weapon,
                 height,birthdate,birthplace,blood_type,description):
        self.uid = uid
        self.full_name = full_name
        self.job = job
        self.age = age
        self.weapon = weapon
        self.height = height
        self.birthdate = birthdate
        self.birthplace = birthplace
        self.blood_type = blood_type
        self.description = description

    def __repr__(self):
        return '<Intro for {0!s}>'.format(self.full_name)
