import sqlite3
from app.models import Viaggio


class TripRepository:
    def __init__(self, db_path='instance/travel.sqlite'):
        self.db_path = db_path

    def get_all_by_user(self, utente_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM viaggi WHERE utente_id = ? ORDER BY data_inizio',
            (utente_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [Viaggio(row[1], row[2], row[3], row[4], row[5], row[6], row[0]) for row in rows]

    def get_by_id(self, viaggio_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM viaggi WHERE id = ?', (viaggio_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Viaggio(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
        return None

    def create(self, viaggio):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO viaggi (utente_id, titolo, data_inizio, data_fine, note) VALUES (?, ?, ?, ?, ?)',
            (viaggio.utente_id, viaggio.titolo, viaggio.data_inizio, viaggio.data_fine, viaggio.note)
        )
        conn.commit()
        conn.close()

    def update(self, viaggio):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE viaggi SET titolo = ?, data_inizio = ?, data_fine = ?, note = ? WHERE id = ?',
            (viaggio.titolo, viaggio.data_inizio, viaggio.data_fine, viaggio.note, viaggio.id)
        )
        conn.commit()
        conn.close()

    def delete(self, viaggio_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM destinazioni WHERE viaggio_id = ?', (viaggio_id,))
        cursor.execute('DELETE FROM viaggi WHERE id = ?', (viaggio_id,))
        conn.commit()
        conn.close()
