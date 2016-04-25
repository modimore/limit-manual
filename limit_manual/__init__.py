from flask import Flask, render_template

from .database.connection import get_connection

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.j2')

# import routes from various files
from .interfaces import enemy
from .interfaces import item
from .interfaces import character
from .interfaces import ability
