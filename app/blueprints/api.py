import requests
from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

NOMINATIM_SEARCH = 'https://nominatim.openstreetmap.org/search'
NOMINATIM_REVERSE = 'https://nominatim.openstreetmap.org/reverse'
OPEN_METEO = 'https://api.open-meteo.com/v1/forecast'
OSRM = 'https://router.project-osrm.org/route/v1/driving'
HEADERS = {'User-Agent': 'TravelPlannerApp/1.0 (progetto-scuola)'}


@api_bp.route('/geocode')
def geocode():
    q = request.args.get('q', '')
    resp = requests.get(NOMINATIM_SEARCH, params={
        'q': q, 'format': 'json', 'limit': 5
    }, headers=HEADERS, timeout=5)
    return jsonify(resp.json())


@api_bp.route('/reverse')
def reverse():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    resp = requests.get(NOMINATIM_REVERSE, params={
        'lat': lat, 'lon': lng, 'format': 'json'
    }, headers=HEADERS, timeout=5)
    return jsonify(resp.json())


@api_bp.route('/weather')
def weather():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    resp = requests.get(OPEN_METEO, params={
        'latitude': lat,
        'longitude': lng,
        'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,sunrise,sunset',
        'forecast_days': 7,
        'timezone': 'auto'
    }, timeout=5)
    return jsonify(resp.json())


@api_bp.route('/route')
def route():
    lat1 = request.args.get('lat1')
    lng1 = request.args.get('lng1')
    lat2 = request.args.get('lat2')
    lng2 = request.args.get('lng2')

    url = f'{OSRM}/{lng1},{lat1};{lng2},{lat2}'
    try:
        resp = requests.get(url, params={
            'overview': 'full',
            'geometries': 'geojson'
        }, timeout=10)
        resp.raise_for_status()
        dati = resp.json()

        if dati.get('code') != 'Ok' or not dati.get('routes'):
            return jsonify({'error': 'Percorso non trovato'}), 200

        r = dati['routes'][0]
        return jsonify({
            'distance_km': round(r['distance'] / 1000, 1),
            'duration_min': round(r['duration'] / 60),
            'geometry': r['geometry']
        })
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Timeout OSRM'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 200
