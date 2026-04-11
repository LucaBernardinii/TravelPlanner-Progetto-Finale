CREATE TABLE IF NOT EXISTS utenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    data_creazione DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS viaggi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utente_id INTEGER NOT NULL,
    titolo TEXT NOT NULL,
    data_inizio TEXT,
    data_fine TEXT,
    note TEXT,
    data_creazione DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utente_id) REFERENCES utenti(id)
);

CREATE TABLE IF NOT EXISTS destinazioni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    viaggio_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    lat REAL,
    lng REAL,
    FOREIGN KEY (viaggio_id) REFERENCES viaggi(id)
);
