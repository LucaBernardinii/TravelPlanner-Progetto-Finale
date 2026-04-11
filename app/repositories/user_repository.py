import sqlite3
from app.models import Utente


class UserRepository:
    def __init__(self, db_path='instance/travel.sqlite'):
        self.db_path = db_path

    def get_by_id(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM utenti WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Utente(row[1], row[2], row[3], row[4], row[0])
        return None

    def get_by_email(self, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM utenti WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Utente(row[1], row[2], row[3], row[4], row[0])
        return None

    def create(self, utente):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO utenti (nome, email, password_hash) VALUES (?, ?, ?)',
            (utente.nome, utente.email, utente.password_hash)
        )
        conn.commit()
        conn.close()
