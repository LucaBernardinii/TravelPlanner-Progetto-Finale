// explore.js — mappa interattiva per la pagina Esplora
// Gestisce: ricerca citta, click su mappa, meteo, POI

var mappa;
var layerPOI = null;
var latCorrente = null;
var lngCorrente = null;


// --- Inizializzazione ---

(function inizializza() {
    mappa = L.map('mappa').setView([41.9, 12.5], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'OpenStreetMap'
    }).addTo(mappa);

    // Click sulla mappa: reverse geocoding
    mappa.on('click', function(e) {
        reverseGeocode(e.latlng.lat, e.latlng.lng);
    });
})();


// --- Ricerca citta ---

function cercaCitta() {
    var q = document.getElementById('citta-input').value.trim();
    if (!q) return;

    fetch('/api/geocode?q=' + encodeURIComponent(q))
        .then(function(r) { return r.json(); })
        .then(function(dati) {
            if (!dati.length) {
                alert('Citta non trovata.');
                return;
            }
            var r = dati[0];
            impostaLocalita(r.display_name, parseFloat(r.lat), parseFloat(r.lon));
        });
}


// --- Reverse geocoding (click su mappa) ---

function reverseGeocode(lat, lng) {
    fetch('/api/reverse?lat=' + lat + '&lng=' + lng)
        .then(function(r) { return r.json(); })
        .then(function(dati) {
            // Usa il nome della citta/comune se disponibile, altrimenti il nome completo
            var addr = dati.address || {};
            var nome = addr.city || addr.town || addr.village || addr.county || dati.display_name;
            document.getElementById('citta-input').value = nome;
            impostaLocalita(dati.display_name, lat, lng);
        });
}


// --- Imposta localita e carica dati ---

function impostaLocalita(nome, lat, lng) {
    latCorrente = lat;
    lngCorrente = lng;

    mappa.setView([lat, lng], 12);

    document.getElementById('nome-citta').textContent = nome;
    document.getElementById('sezione-risultati').style.display = 'block';

    // Rimuove POI precedenti se presenti
    if (layerPOI) {
        mappa.removeLayer(layerPOI);
        layerPOI = null;
        document.getElementById('lista-poi').innerHTML = '';
    }

    caricaMeteo(lat, lng);
}


// --- Meteo ---

function caricaMeteo(lat, lng) {
    var tbody = document.getElementById('corpo-meteo');
    tbody.innerHTML = '<tr><td colspan="4">Caricamento...</td></tr>';

    fetch('/api/weather?lat=' + lat + '&lng=' + lng)
        .then(function(r) { return r.json(); })
        .then(function(dati) {
            tbody.innerHTML = '';
            var g = dati.daily;
            for (var i = 0; i < g.time.length; i++) {
                var tr = document.createElement('tr');
                tr.innerHTML =
                    '<td>' + g.time[i] + '</td>' +
                    '<td>' + g.temperature_2m_min[i] + '</td>' +
                    '<td>' + g.temperature_2m_max[i] + '</td>' +
                    '<td>' + g.precipitation_sum[i] + '</td>';
                tbody.appendChild(tr);
            }
        });
}


// --- Punti di interesse ---

function cercaPOI() {
    if (!latCorrente) {
        alert('Cerca prima una citta.');
        return;
    }

    var tipo = document.getElementById('tipo-poi').value;
    var raggio = document.getElementById('raggio-poi').value;
    var lista = document.getElementById('lista-poi');
    lista.innerHTML = '<li>Caricamento...</li>';

    // Rimuove il layer POI precedente dalla mappa
    if (layerPOI) {
        mappa.removeLayer(layerPOI);
    }
    layerPOI = L.layerGroup().addTo(mappa);

    fetch('/api/poi?lat=' + latCorrente + '&lng=' + lngCorrente + '&tipo=' + tipo + '&raggio=' + raggio)
        .then(function(r) { return r.json(); })
        .then(function(dati) {
            lista.innerHTML = '';
            var elementi = dati.elements || [];

            if (!elementi.length) {
                lista.innerHTML = '<li>Nessun risultato nel raggio selezionato.</li>';
                return;
            }

            elementi.forEach(function(el) {
                var nome = (el.tags && el.tags.name) ? el.tags.name : 'Senza nome';

                // Aggiunge voce alla lista nel pannello
                var li = document.createElement('li');
                li.textContent = nome;
                lista.appendChild(li);

                // Aggiunge marcatore sulla mappa
                if (el.lat && el.lon) {
                    L.marker([el.lat, el.lon])
                        .addTo(layerPOI)
                        .bindPopup(nome);
                }
            });
        });
}
