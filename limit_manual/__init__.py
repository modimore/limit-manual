# Basic Flask & Jinja2 related imports
from flask import Flask, render_template

# Create Application
app = Flask(__name__)
app.config.from_object('limit_manual.config.DevConfig')

from .assets import assets

# Import function to connect to database (must be done after app is created)
from .database.connection import get_connection

@app.route('/')
def welcome():
    return render_template('welcome.j2')

# import routes from various files
from .interfaces import enemy
from .interfaces import item
from .interfaces import character
from .interfaces import ability
