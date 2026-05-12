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
        # colonne: id(0) viaggio_id(1) nome(2) lat(3) lng(4) data_arrivo(5) data_partenza(6)
        return [
            Destinazione(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
            for row in rows
        ]

    def add(self, destinazione):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO destinazioni (viaggio_id, nome, lat, lng, data_arrivo, data_partenza) '
            'VALUES (?, ?, ?, ?, ?, ?)',
            (destinazione.viaggio_id, destinazione.nome,
             destinazione.lat, destinazione.lng,
             destinazione.data_arrivo, destinazione.data_partenza)
        )
        conn.commit()
        conn.close()

    def delete(self, dest_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM attivita WHERE destinazione_id = ?', (dest_id,))
        cursor.execute('DELETE FROM destinazioni WHERE id = ?', (dest_id,))
        conn.commit()
        conn.close()
