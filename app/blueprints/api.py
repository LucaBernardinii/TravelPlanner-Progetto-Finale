import requests
from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

NOMINATIM_SEARCH = 'https://nominatim.openstreetmap.org/search'
NOMINATIM_REVERSE = 'https://nominatim.openstreetmap.org/reverse'
OPEN_METEO = 'https://api.open-meteo.com/v1/forecast'
OVERPASS = 'https://overpass-api.de/api/interpreter'
HEADERS = {'User-Agent': 'TravelPlannerApp/1.0 (progetto-scuola)'}


@api_bp.route('/geocode')
def geocode():
    """Converte il nome di una citta in coordinate lat/lng."""
    q = request.args.get('q', '')
    resp = requests.get(NOMINATIM_SEARCH, params={
        'q': q, 'format': 'json', 'limit': 5
    }, headers=HEADERS, timeout=5)
    return jsonify(resp.json())


@api_bp.route('/reverse')
def reverse():
    """Converte coordinate lat/lng nel nome del luogo (reverse geocoding)."""
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    resp = requests.get(NOMINATIM_REVERSE, params={
        'lat': lat, 'lon': lng, 'format': 'json'
    }, headers=HEADERS, timeout=5)
    return jsonify(resp.json())


@api_bp.route('/weather')
def weather():
    """Restituisce le previsioni meteo a 7 giorni tramite Open-Meteo."""
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    resp = requests.get(OPEN_METEO, params={
        'latitude': lat,
        'longitude': lng,
        'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
        'forecast_days': 7,
        'timezone': 'auto'
    }, timeout=5)
    return jsonify(resp.json())


@api_bp.route('/poi')
def poi():
    """Cerca punti di interesse tramite Overpass API (dati OpenStreetMap)."""
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    tipo = request.args.get('tipo', 'tourism')
    raggio = request.args.get('raggio', 1000)
    query = f'[out:json];node["{tipo}"](around:{raggio},{lat},{lng});out 20;'
    resp = requests.post(OVERPASS, data={'data': query}, timeout=10)
    return jsonify(resp.json())
