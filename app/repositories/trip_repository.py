import sqlite3
from app.models import Viaggio


class TripRepository:
    def __init__(self, db_path='instance/travel.sqlite'):
        self.db_path = db_path

    # Query con colonne esplicite per evitare problemi di ordinamento
    # dopo le migrazioni ALTER TABLE
    COLONNE = (
        'id, utente_id, titolo, data_inizio, data_fine, note, '
        'COALESCE(condiviso, 0) AS condiviso, data_creazione'
    )

    def _riga_a_viaggio(self, row):
        # row: id(0) utente_id(1) titolo(2) data_inizio(3) data_fine(4)
        #      note(5) condiviso(6) data_creazione(7)
        return Viaggio(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[0])

    def get_all_by_user(self, utente_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT {self.COLONNE} FROM viaggi '
            'WHERE utente_id = ? ORDER BY data_inizio',
            (utente_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [self._riga_a_viaggio(r) for r in rows]

    def get_all_shared(self):
        """Restituisce tutti i viaggi condivisi, ordinati per data di creazione."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT {self.COLONNE} FROM viaggi '
            'WHERE COALESCE(condiviso, 0) = 1 ORDER BY data_creazione DESC'
        )
        rows = cursor.fetchall()
        conn.close()
        return [self._riga_a_viaggio(r) for r in rows]

    def get_by_id(self, viaggio_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT {self.COLONNE} FROM viaggi WHERE id = ?',
            (viaggio_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return self._riga_a_viaggio(row) if row else None

    def create(self, viaggio):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO viaggi (utente_id, titolo, data_inizio, data_fine, note, condiviso) '
            'VALUES (?, ?, ?, ?, ?, 0)',
            (viaggio.utente_id, viaggio.titolo,
             viaggio.data_inizio, viaggio.data_fine, viaggio.note)
        )
        conn.commit()
        conn.close()

    def update(self, viaggio):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE viaggi SET titolo=?, data_inizio=?, data_fine=?, note=? WHERE id=?',
            (viaggio.titolo, viaggio.data_inizio, viaggio.data_fine, viaggio.note, viaggio.id)
        )
        conn.commit()
        conn.close()

    def set_condiviso(self, viaggio_id, condiviso):
        """Imposta il flag di condivisione (0 = privato, 1 = condiviso)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE viaggi SET condiviso=? WHERE id=?',
            (condiviso, viaggio_id)
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
