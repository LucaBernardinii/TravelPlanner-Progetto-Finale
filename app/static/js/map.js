// map.js — mappa interattiva per la pagina dettaglio viaggio
// Modalita click: 'destinazione' (default) oppure 'attivita' (quando un form attivita e aperto)

var mappa;
var marcatoreTemp = null;
var marcatoreAttTemp = null;
var layerPercorsi = null;

// Modalita corrente della mappa e destinazione attiva
var modoMappa = 'destinazione';
var destIdAttivo = null;

// Icone quadrate per le attivita (si distinguono dai marcatori rotondi delle citta)
var ICONE_ATTIVITA = {
    hotel:      creaIcona('H', 'marker-hotel'),
    ristorante: creaIcona('R', 'marker-ristorante'),
    museo:      creaIcona('M', 'marker-museo'),
    attrazione: creaIcona('A', 'marker-attrazione'),
    trasporto:  creaIcona('T', 'marker-trasporto'),
    generale:   creaIcona('G', 'marker-generale'),
};

function creaIcona(lettera, classe) {
    return L.divIcon({
        className: 'marker-att ' + classe,
        html: lettera,
        iconSize: [22, 22],
        iconAnchor: [11, 11],
        popupAnchor: [0, -11]
    });
}


// --- Inizializzazione ---

(function inizializza() {
    mappa = L.map('mappa');
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'OpenStreetMap'
    }).addTo(mappa);

    layerPercorsi = L.layerGroup().addTo(mappa);

    var marcatoriCitta = [];

    DESTINAZIONI.forEach(function(dest) {
        // Marcatore citta (stile Leaflet default — goccia blu)
        if (dest.lat && dest.lng) {
            var popup = '<strong>' + dest.nome + '</strong>';
            if (dest.data_arrivo || dest.data_partenza) {
                popup += '<br><small>' +
                    (dest.data_arrivo || '') +
                    (dest.data_arrivo && dest.data_partenza ? ' - ' : '') +
                    (dest.data_partenza || '') + '</small>';
            }
            var m = L.marker([dest.lat, dest.lng]).addTo(mappa).bindPopup(popup);
            marcatoriCitta.push(m);
        }

        // Marcatori attivita (icone quadrate colorate)
        dest.attivita.forEach(function(att) {
            if (att.lat && att.lng) {
                var icona = ICONE_ATTIVITA[att.tipo] || ICONE_ATTIVITA.generale;
                L.marker([att.lat, att.lng], { icon: icona })
                    .addTo(mappa)
                    .bindPopup('<strong>' + att.nome + '</strong>');
            }
        });
    });

    // Centra la vista sulle destinazioni esistenti
    if (marcatoriCitta.length > 0) {
        mappa.fitBounds(L.featureGroup(marcatoriCitta).getBounds().pad(0.3));
    } else {
        mappa.setView([41.9, 12.5], 5);
    }

    caricaPercorsi();
    setupToggleListeners();

    // Click sulla mappa: comportamento in base alla modalita corrente
    mappa.on('click', function(e) {
        if (modoMappa === 'attivita' && destIdAttivo) {
            impostaPosizioneAttivita(e.latlng.lat, e.latlng.lng, destIdAttivo);
        } else {
            reverseGeocode(e.latlng.lat, e.latlng.lng);
        }
    });
})();


// --- Toggle modalita: apre/chiude form attivita ---

function setupToggleListeners() {
    var stato = document.getElementById('stato-mappa');

    document.querySelectorAll('.aggiungi-att').forEach(function(det) {
        det.addEventListener('toggle', function() {
            if (det.open) {
                // Entra in modalita attivita
                modoMappa = 'attivita';
                destIdAttivo = det.dataset.destId;
                // Rimuove marcatore destinazione temporaneo se presente
                if (marcatoreTemp) { mappa.removeLayer(marcatoreTemp); marcatoreTemp = null; }
                if (stato) stato.textContent = 'Clicca sulla mappa per posizionare l\'attivita';
            } else {
                // Torna in modalita destinazione
                modoMappa = 'destinazione';
                destIdAttivo = null;
                // Rimuove marcatore attivita temporaneo
                if (marcatoreAttTemp) { mappa.removeLayer(marcatoreAttTemp); marcatoreAttTemp = null; }
                if (stato) stato.textContent = 'Clicca sulla mappa per aggiungere una destinazione';
            }
        });
    });
}


// --- Posizionamento attivita sulla mappa ---

function impostaPosizioneAttivita(lat, lng, destId) {
    // Aggiorna i campi nascosti del form attivita
    var campoLat = document.getElementById('att-lat-' + destId);
    var campoLng = document.getElementById('att-lng-' + destId);
    var etichetta = document.getElementById('att-pos-' + destId);

    if (campoLat) campoLat.value = lat;
    if (campoLng) campoLng.value = lng;
    if (etichetta) etichetta.textContent = 'Posizione: ' + lat.toFixed(5) + ', ' + lng.toFixed(5);

    // Marcatore temporaneo con stile attivita
    if (marcatoreAttTemp) mappa.removeLayer(marcatoreAttTemp);
    marcatoreAttTemp = L.marker([lat, lng], { icon: creaIcona('+', 'marker-temp') })
        .addTo(mappa)
        .bindPopup('Posizione attivita').openPopup();
}


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
                        L.geoJSON(dati.geometry, {
                            style: { color: '#3388ff', weight: 3, opacity: 0.7 }
                        }).addTo(layerPercorsi);
                    }
                    aggiornaDistanza(d1.id, d2.id, dati);
                })
                .catch(function() { aggiornaDistanza(d1.id, d2.id, null); });
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
            if (!dati.length) { contenitore.innerHTML = '<p>Nessun risultato.</p>'; return; }
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


// --- Reverse geocoding (click in modalita destinazione) ---

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

    // Apre il pannello aggiungi destinazione se non e gia aperto
    var wrapper = document.getElementById('form-dest-wrapper');
    if (wrapper && !wrapper.open) wrapper.open = true;
}
