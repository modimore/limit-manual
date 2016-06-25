# Basic Flask & Jinja2 related imports
from flask import Flask, render_template

# Create application instance
app = Flask(__name__)
app.config.from_object('limit_manual.config.DevConfig')

# Import asset management object
from .assets import assets

# Import function to connect to database
from .database import get_connection

@app.route('/')
def welcome():
    return render_template('welcome.j2')

# import routes from various files
from .interfaces import enemy
from .interfaces import item
from .interfaces import character
from .interfaces import ability
