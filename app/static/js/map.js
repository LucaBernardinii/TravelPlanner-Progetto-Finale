// map.js — mappa interattiva per la pagina dettaglio viaggio
// Gestisce: visualizzazione destinazioni, ricerca citta, click sulla mappa

var mappa;
var marcatoreTemp = null;

// --- Inizializzazione ---

(function inizializza() {
    mappa = L.map('mappa');

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'OpenStreetMap'
    }).addTo(mappa);

    // Aggiunge i marcatori delle destinazioni gia salvate
    var marcatori = [];
    DESTINAZIONI.forEach(function(dest) {
        if (dest.lat && dest.lng) {
            var m = L.marker([dest.lat, dest.lng])
                .addTo(mappa)
                .bindPopup(dest.nome);
            marcatori.push(m);
        }
    });

    // Centra la mappa sulle destinazioni esistenti o sull'Italia
    if (marcatori.length > 0) {
        mappa.fitBounds(L.featureGroup(marcatori).getBounds().pad(0.3));
    } else {
        mappa.setView([41.9, 12.5], 5);
    }

    // Click sulla mappa: reverse geocoding e precompilazione form
    mappa.on('click', function(e) {
        reverseGeocode(e.latlng.lat, e.latlng.lng);
    });
})();


// --- Ricerca citta ---

function cercaCitta() {
    var q = document.getElementById('cerca-citta').value.trim();
    if (!q) return;

    var contenitore = document.getElementById('risultati-ricerca');
    contenitore.innerHTML = '<p>Ricerca in corso...</p>';

    fetch('/api/geocode?q=' + encodeURIComponent(q))
        .then(function(r) { return r.json(); })
        .then(function(dati) {
            contenitore.innerHTML = '';
            if (!dati.length) {
                contenitore.innerHTML = '<p>Nessun risultato.</p>';
                return;
            }
            dati.forEach(function(r) {
                var btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'risultato-btn';
                btn.textContent = r.display_name;
                btn.onclick = function() {
                    selezionaDestinazione(r.display_name, parseFloat(r.lat), parseFloat(r.lon));
                    contenitore.innerHTML = '';
                };
                contenitore.appendChild(btn);
            });
        });
}


// --- Reverse geocoding (click su mappa) ---

function reverseGeocode(lat, lng) {
    fetch('/api/reverse?lat=' + lat + '&lng=' + lng)
        .then(function(r) { return r.json(); })
        .then(function(dati) {
            var nome = dati.display_name || ('Lat ' + lat.toFixed(4) + ', Lng ' + lng.toFixed(4));
            selezionaDestinazione(nome, lat, lng);
        });
}


// --- Selezione destinazione (da ricerca o da click) ---

function selezionaDestinazione(nome, lat, lng) {
    // Rimuove il marcatore temporaneo precedente
    if (marcatoreTemp) {
        mappa.removeLayer(marcatoreTemp);
    }

    marcatoreTemp = L.marker([lat, lng]).addTo(mappa).bindPopup(nome).openPopup();
    mappa.setView([lat, lng], 10);

    // Precompila i campi nascosti del form
    document.getElementById('nome').value = nome;
    document.getElementById('lat').value = lat;
    document.getElementById('lng').value = lng;
    document.getElementById('btn-aggiungi').disabled = false;

    // Mostra l'anteprima del nome nel pannello
    var anteprima = document.getElementById('anteprima-dest');
    anteprima.innerHTML = '<p><strong>Selezionata:</strong> ' + nome + '</p>';
}
