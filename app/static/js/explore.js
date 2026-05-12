// explore.js — mappa interattiva per la pagina Esplora

var mappa;
var marcatoreCorrente = null;
var layerPOI = null;
var latCorrente = null;
var lngCorrente = null;
var nomeCittaCorrente = '';


(function inizializza() {
    mappa = L.map('mappa').setView([41.9, 12.5], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'OpenStreetMap'
    }).addTo(mappa);

    mappa.on('click', function(e) {
        reverseGeocode(e.latlng.lat, e.latlng.lng);
    });

    var formAggiungi = document.getElementById('form-aggiungi-dest');
    if (formAggiungi) {
        formAggiungi.addEventListener('submit', function() {
            var tripId = document.getElementById('select-viaggio').value;
            this.action = '/trips/' + tripId + '/destinazioni/add';
            document.getElementById('dest-nome').value = nomeCittaCorrente;
            document.getElementById('dest-lat').value = latCorrente;
            document.getElementById('dest-lng').value = lngCorrente;
            document.getElementById('dest-next').value =
                '/explore?citta=' + encodeURIComponent(nomeCittaCorrente);
        });
    }

    var params = new URLSearchParams(window.location.search);
    var citta = params.get('citta');
    if (citta) {
        document.getElementById('citta-input').value = citta;
        cercaCitta();
    }
})();


function cercaCitta() {
    var q = document.getElementById('citta-input').value.trim();
    if (!q) return;
    fetch('/api/geocode?q=' + encodeURIComponent(q))
        .then(function(r) { return r.json(); })
        .then(function(dati) {
            if (!dati.length) { alert('Citta non trovata.'); return; }
            var r = dati[0];
            impostaLocalita(r.display_name, parseFloat(r.lat), parseFloat(r.lon));
        })
        .catch(function() { alert('Errore durante la ricerca.'); });
}


function reverseGeocode(lat, lng) {
    fetch('/api/reverse?lat=' + lat + '&lng=' + lng)
        .then(function(r) { return r.json(); })
        .then(function(dati) {
            var addr = dati.address || {};
            var nome = addr.city || addr.town || addr.village || addr.county || dati.display_name;
            document.getElementById('citta-input').value = nome;
            impostaLocalita(dati.display_name, lat, lng);
        });
}


function impostaLocalita(nomeCompleto, lat, lng) {
    latCorrente = lat;
    lngCorrente = lng;
    nomeCittaCorrente = nomeCompleto;

    mappa.setView([lat, lng], 12);
    if (marcatoreCorrente) mappa.removeLayer(marcatoreCorrente);
    marcatoreCorrente = L.marker([lat, lng]).addTo(mappa)
        .bindPopup(nomeCompleto).openPopup();

    document.getElementById('nome-citta').textContent = nomeCompleto;
    document.getElementById('sezione-risultati').style.display = 'block';

    if (layerPOI) { mappa.removeLayer(layerPOI); layerPOI = null; }
    document.getElementById('lista-poi').innerHTML = '';

    caricaMeteo(lat, lng);
}


function caricaMeteo(lat, lng) {
    var tbody = document.getElementById('corpo-meteo');
    tbody.innerHTML = '<tr><td colspan="6">Caricamento...</td></tr>';

    fetch('/api/weather?lat=' + lat + '&lng=' + lng)
        .then(function(r) { return r.json(); })
        .then(function(dati) {
            tbody.innerHTML = '';
            var g = dati.daily;
            if (!g || !g.time) {
                tbody.innerHTML = '<tr><td colspan="6">Dati non disponibili.</td></tr>';
                return;
            }
            for (var i = 0; i < g.time.length; i++) {
                // Alba e tramonto arrivano come "2026-05-10T06:23" — estrae solo l'orario
                var alba = g.sunrise && g.sunrise[i]
                    ? g.sunrise[i].split('T')[1] : '-';
                var tramonto = g.sunset && g.sunset[i]
                    ? g.sunset[i].split('T')[1] : '-';

                var tr = document.createElement('tr');
                tr.innerHTML =
                    '<td>' + g.time[i] + '</td>' +
                    '<td>' + g.temperature_2m_min[i] + ' C</td>' +
                    '<td>' + g.temperature_2m_max[i] + ' C</td>' +
                    '<td>' + (g.precipitation_sum[i] || 0) + ' mm</td>' +
                    '<td>' + alba + '</td>' +
                    '<td>' + tramonto + '</td>';
                tbody.appendChild(tr);
            }
        })
        .catch(function() {
            tbody.innerHTML = '<tr><td colspan="6">Errore caricamento meteo.</td></tr>';
        });
}


function cercaPOI() {
    if (!latCorrente) { alert('Cerca prima una citta.'); return; }

    var tipo = document.getElementById('tipo-poi').value;
    var raggio = document.getElementById('raggio-poi').value;
    var lista = document.getElementById('lista-poi');
    lista.innerHTML = '<li>Ricerca in corso...</li>';

    if (layerPOI) mappa.removeLayer(layerPOI);
    layerPOI = L.layerGroup().addTo(mappa);

    fetch('/api/poi?lat=' + latCorrente + '&lng=' + lngCorrente +
          '&tipo=' + tipo + '&raggio=' + raggio)
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
                var elLat = el.lat || (el.center && el.center.lat);
                var elLng = el.lon || (el.center && el.center.lon);

                var li = document.createElement('li');
                li.className = 'poi-voce';
                li.textContent = nome;

                if (elLat && elLng) {
                    var marcatore = L.marker([elLat, elLng])
                        .addTo(layerPOI).bindPopup(nome);
                    li.style.cursor = 'pointer';
                    li.addEventListener('click', function() {
                        mappa.setView([elLat, elLng], 16);
                        marcatore.openPopup();
                    });
                }
                lista.appendChild(li);
            });
        })
        .catch(function() {
            lista.innerHTML = '<li>Errore durante la ricerca.</li>';
        });
}
