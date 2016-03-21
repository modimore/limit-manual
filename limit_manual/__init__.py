from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/limit_manual.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # deactivate explicitly later
db = SQLAlchemy(app)

@app.route('/')
def welcome():
    return render_template('welcome.j2')

# Import routes with enemy-related interfaces
from .interfaces import enemy
from .interfaces import item
from .interfaces import character
from .interfaces import action
