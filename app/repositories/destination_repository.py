import sqlite3
from app.models import Destinazione


class DestinationRepository:
    def __init__(self, db_path='instance/travel.sqlite'):
        self.db_path = db_path

    def get_by_trip(self, viaggio_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM destinazioni WHERE viaggio_id = ?', (viaggio_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Destinazione(row[1], row[2], row[3], row[4], row[0]) for row in rows]

    def add(self, destinazione):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO destinazioni (viaggio_id, nome, lat, lng) VALUES (?, ?, ?, ?)',
            (destinazione.viaggio_id, destinazione.nome, destinazione.lat, destinazione.lng)
        )
        conn.commit()
        conn.close()

    def delete(self, dest_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM destinazioni WHERE id = ?', (dest_id,))
        conn.commit()
        conn.close()
