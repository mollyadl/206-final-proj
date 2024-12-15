
import sqlite3
import requests

def make_table(dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS apistats (
                   date INTEGER PRIMARY KEY,
                   cases INTEGER,
                   deaths INTEGER,
                   recovered INTEGER,
                   active INTEGER
                   )
    ''')

    conn.commit()

    #cases
    #deaths
    #recovered
    #active