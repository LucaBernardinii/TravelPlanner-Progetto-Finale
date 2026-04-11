class Utente:
    def __init__(self, nome, email, password_hash, data_creazione=None, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.password_hash = password_hash
        self.data_creazione = data_creazione


class Viaggio:
    def __init__(self, utente_id, titolo, data_inizio, data_fine, note=None, data_creazione=None, id=None):
        self.id = id
        self.utente_id = utente_id
        self.titolo = titolo
        self.data_inizio = data_inizio
        self.data_fine = data_fine
        self.note = note
        self.data_creazione = data_creazione


class Destinazione:
    def __init__(self, viaggio_id, nome, lat=None, lng=None, id=None):
        self.id = id
        self.viaggio_id = viaggio_id
        self.nome = nome
        self.lat = lat
        self.lng = lng
