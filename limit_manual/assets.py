'''
Uses Flask-Assets package to monitor and compile "static" assets.
Currently requires 'sass' Ruby gem on your system.
'''

import os.path

from flask.ext.assets import Environment, Bundle
from . import app

assets = Environment(app)

# Main Site Styles
css_main = Bundle('scss/main/general.scss',
                  'scss/main/layout.scss',
                  'scss/main/tables.scss',
                  filters='scss',
                  output='css/main.css'
                 )
assets.register('css_main', css_main)

# Ability Pages
css_ability = Bundle('scss/ability.scss',
                     filters='scss',
                     output='css/ability.css'
                    )
assets.register('css_ability', css_ability)

# Character Pages
css_character = Bundle('scss/character.scss',
                        filters='scss',
                        output='css/character.css'
                       )
assets.register('css_character', css_character)

# Enemy Pages
css_enemy = Bundle('scss/enemy.scss',
                   filters='scss',
                   output='css/enemy.css'
                  )
assets.register('css_enemy', css_enemy)

# Item Pages
css_item = Bundle('item.scss',
                   filters='scss',
                   output='css/item.css'
                  )
assets.register('css_item', css_item)
