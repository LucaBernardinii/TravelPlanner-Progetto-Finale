import sqlite3
from app.models import Attivita


class AttivitaRepository:
    def __init__(self, db_path='instance/travel.sqlite'):
        self.db_path = db_path

    def get_by_destination(self, destinazione_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM attivita WHERE destinazione_id = ?', (destinazione_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        # colonne: id(0) destinazione_id(1) nome(2) tipo(3)
        return [Attivita(row[1], row[2], row[3], row[0]) for row in rows]

    def add(self, attivita):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO attivita (destinazione_id, nome, tipo) VALUES (?, ?, ?)',
            (attivita.destinazione_id, attivita.nome, attivita.tipo)
        )
        conn.commit()
        conn.close()

    def delete(self, attivita_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM attivita WHERE id = ?', (attivita_id,))
        conn.commit()
        conn.close()
