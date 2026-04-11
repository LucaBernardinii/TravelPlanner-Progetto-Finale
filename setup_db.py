import sqlite3
import os


DB_PATH = 'instance/travel.sqlite'
SCHEMA_PATH = 'app/schema.sql'


def setup():
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    conn.close()
    print('Database inizializzato:', DB_PATH)


if __name__ == '__main__':
    setup()
