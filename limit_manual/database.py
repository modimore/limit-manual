from . import app

def get_connection():
    import psycopg2
    return psycopg2.connect(dbname=app.config['DB_NAME'],
                            user=app.config['DB_USER']
                            )
