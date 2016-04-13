import sqlite3

def get_connection():
    import os
    db_path = os.path.dirname(__file__)
    db_loc = os.path.join(db_path,"limit_manual.db")
    return sqlite3.connect(db_loc)
