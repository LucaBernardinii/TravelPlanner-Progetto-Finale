// map.js — mappa interattiva per la pagina dettaglio viaggio
// Gestisce: marcatori destinazioni, percorsi OSRM, ricerca citta, click su mappa

var mappa;
var marcatoreTemp = null;
var layerPercorsi = null;


// --- Inizializzazione ---

(function inizializza() {
    mappa = L.map('mappa');
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'OpenStreetMap'
    }).addTo(mappa);

    layerPercorsi = L.layerGroup().addTo(mappa);

    // Aggiunge i marcatori delle destinazioni salvate
    var marcatori = [];
    DESTINAZIONI.forEach(function(dest) {
        if (dest.lat && dest.lng) {
            var popup = dest.nome;
            if (dest.data_arrivo || dest.data_partenza) {
                popup += '<br><small>' +
                    (dest.data_arrivo || '') +
                    (dest.data_arrivo && dest.data_partenza ? ' - ' : '') +
                    (dest.data_partenza || '') +
                    '</small>';
            }
            var m = L.marker([dest.lat, dest.lng])
                .addTo(mappa)
                .bindPopup(popup);
            marcatori.push(m);
        }
    });

    if (marcatori.length > 0) {
        mappa.fitBounds(L.featureGroup(marcatori).getBounds().pad(0.3));
    } else {
        mappa.setView([41.9, 12.5], 5);
    }

    // Percorsi OSRM tra destinazioni consecutive
    caricaPercorsi();

    // Click sulla mappa: reverse geocoding
    mappa.on('click', function(e) {
        reverseGeocode(e.latlng.lat, e.latlng.lng);
    });
})();


// --- Percorsi OSRM tra destinazioni consecutive ---

function caricaPercorsi() {
    for (var i = 0; i < DESTINAZIONI.length - 1; i++) {
        (function(d1, d2) {
            if (!d1.lat || !d1.lng || !d2.lat || !d2.lng) {
                aggiornaDistanza(d1.id, d2.id, null);
                return;
            }
            fetch('/api/route?lat1=' + d1.lat + '&lng1=' + d1.lng +
                  '&lat2=' + d2.lat + '&lng2=' + d2.lng)
                .then(function(r) { return r.json(); })
                .then(function(dati) {
                    if (dati.geometry) {
                        // Disegna il percorso sulla mappa
                        L.geoJSON(dati.geometry, {
                            style: { color: '#3388ff', weight: 3, opacity: 0.7 }
                        }).addTo(layerPercorsi);
                    }
                    aggiornaDistanza(d1.id, d2.id, dati);
                })
                .catch(function() {
                    aggiornaDistanza(d1.id, d2.id, null);
                });
        })(DESTINAZIONI[i], DESTINAZIONI[i + 1]);
    }
}

function aggiornaDistanza(id1, id2, dati) {
    var el = document.getElementById('dist-' + id1 + '-' + id2);
    if (!el) return;
    if (!dati || dati.error) {
        el.textContent = 'Percorso non disponibile';
    } else {
        el.textContent = dati.distance_km + ' km — ' + dati.duration_min + ' min';
    }
}


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


// --- Reverse geocoding (click sulla mappa) ---

function reverseGeocode(lat, lng) {
    fetch('/api/reverse?lat=' + lat + '&lng=' + lng)
        .then(function(r) { return r.json(); })
        .then(function(dati) {
            var nome = dati.display_name || ('Lat ' + lat.toFixed(4) + ', Lng ' + lng.toFixed(4));
            selezionaDestinazione(nome, lat, lng);
        });
}


// --- Selezione destinazione ---

function selezionaDestinazione(nome, lat, lng) {
    if (marcatoreTemp) mappa.removeLayer(marcatoreTemp);

    marcatoreTemp = L.marker([lat, lng]).addTo(mappa).bindPopup(nome).openPopup();
    mappa.setView([lat, lng], 10);

    document.getElementById('nome').value = nome;
    document.getElementById('lat').value = lat;
    document.getElementById('lng').value = lng;
    document.getElementById('btn-aggiungi').disabled = false;
    document.getElementById('anteprima-dest').innerHTML =
        '<p><strong>Selezionata:</strong> ' + nome + '</p>';
}
