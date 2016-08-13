'''
Database connection module
'''

from . import app

def get_connection():
    ''' connect to postgres database specified by app configuration. '''
    import psycopg2
    return psycopg2.connect(dbname=app.config['DB_NAME'],
                            user=app.config['DB_USER']
                            )
