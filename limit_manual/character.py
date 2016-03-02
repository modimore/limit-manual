# This file is nowhere near functional, but I know I will need it in the future
# The relations to represent this information have not been worked out yet

from flask import render_template

from limit_manual import app, db

class Character(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
