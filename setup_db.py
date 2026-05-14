import sqlite3
import os

DB_PATH = 'instance/travel.sqlite'
SCHEMA_PATH = 'app/schema.sql'


def setup():
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())

    # Migrazione per database esistenti
    cursor = conn.cursor()
    migrazioni = [
        'ALTER TABLE destinazioni ADD COLUMN data_arrivo TEXT',
        'ALTER TABLE destinazioni ADD COLUMN data_partenza TEXT',
        'ALTER TABLE attivita ADD COLUMN lat REAL',
        'ALTER TABLE attivita ADD COLUMN lng REAL',
    ]
    for sql in migrazioni:
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception:
            pass

    conn.close()
    print('Database inizializzato:', DB_PATH)


if __name__ == '__main__':
    setup()
