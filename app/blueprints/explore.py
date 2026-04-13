from flask import Blueprint, render_template, request, redirect, url_for, session
import requests

explore_bp = Blueprint('explore', __name__)

NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search'
OPEN_METEO_URL = 'https://api.open-meteo.com/v1/forecast'
OVERPASS_URL = 'https://overpass-api.de/api/interpreter'
HEADERS = {'User-Agent': 'TravelPlannerApp/1.0 (progetto-scuola)'}


@explore_bp.route('/explore', methods=['GET', 'POST'])
def search():
    if 'utente_id' not in session:
        return redirect(url_for('auth.login'))
    citta = ''
    meteo = None
    poi = []
    lat = None
    lng = None
    nome_citta = ''
    errore = None

    tipo_poi = request.form.get('tipo_poi', 'tourism')
    raggio = request.form.get('raggio', '1000')

    if request.method == 'POST' and request.form.get('query'):
        citta = request.form.get('query', '')

        # Geocoding della citta
        resp = requests.get(NOMINATIM_URL, params={
            'q': citta, 'format': 'json', 'limit': 1
        }, headers=HEADERS, timeout=5)
        risultati = resp.json()

        if not risultati:
            errore = 'Citta non trovata.'
        else:
            lat = float(risultati[0]['lat'])
            lng = float(risultati[0]['lon'])
            nome_citta = risultati[0]['display_name']

            # Previsioni meteo per 7 giorni
            resp_meteo = requests.get(OPEN_METEO_URL, params={
                'latitude': lat,
                'longitude': lng,
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode',
                'forecast_days': 7,
                'timezone': 'auto'
            }, timeout=5)
            dati_meteo = resp_meteo.json()

            # Costruisce lista di dizionari per il template
            giorni = dati_meteo.get('daily', {})
            meteo = []
            for i in range(len(giorni.get('time', []))):
                meteo.append({
                    'data': giorni['time'][i],
                    'min': giorni['temperature_2m_min'][i],
                    'max': giorni['temperature_2m_max'][i],
                    'pioggia': giorni['precipitation_sum'][i],
                })

            # Punti di interesse tramite Overpass
            query_overpass = f'[out:json];node["{tipo_poi}"](around:{raggio},{lat},{lng});out 20;'
            resp_poi = requests.post(OVERPASS_URL, data={'data': query_overpass}, timeout=10)
            elementi = resp_poi.json().get('elements', [])

            for el in elementi:
                nome = el.get('tags', {}).get('name', 'Senza nome')
                poi.append({
                    'nome': nome,
                    'tipo': el.get('tags', {}).get(tipo_poi, ''),
                    'lat': el.get('lat'),
                    'lng': el.get('lon'),
                    'osm_link': f"https://www.openstreetmap.org/node/{el['id']}"
                })

    return render_template('explore/search.html',
                           citta=citta,
                           nome_citta=nome_citta,
                           meteo=meteo,
                           poi=poi,
                           lat=lat,
                           lng=lng,
                           tipo_poi=tipo_poi,
                           raggio=raggio,
                           errore=errore)
