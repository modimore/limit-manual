'''
Uses Flask-Assets package to monitor and compile "static" assets.
'''


from flask_assets import Environment, Bundle
from . import app

assets = Environment(app)

css_main = Bundle('scss/main/general.scss',
                  'scss/main/layout.scss',
                  'scss/main/grid.scss',
                  'scss/main/tables.scss',
                  filters='pyscss',
                  output='css/main.css'
                 )
assets.register('css_main', css_main)

css_ability = Bundle('scss/ability.scss',
                     filters='pyscss',
                     output='css/ability.css'
                    )
assets.register('css_ability', css_ability)

css_character = Bundle('scss/character.scss',
                        filters='pyscss',
                        output='css/character.css'
                       )
assets.register('css_character', css_character)

css_enemy = Bundle('scss/enemy.scss',
                   filters='pyscss',
                   output='css/enemy.css'
                  )
assets.register('css_enemy', css_enemy)

css_item = Bundle('scss/item.scss',
                   filters='pyscss',
                   output='css/item.css'
                  )
assets.register('css_item', css_item)
