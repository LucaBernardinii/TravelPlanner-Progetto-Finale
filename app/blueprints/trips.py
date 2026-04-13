from flask import Blueprint, render_template, request, redirect, url_for, session, abort
import requests

from app.models import Viaggio, Destinazione
from app.repositories.trip_repository import TripRepository
from app.repositories.destination_repository import DestinationRepository

trips_bp = Blueprint('trips', __name__)

NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search'
HEADERS = {'User-Agent': 'TravelPlannerApp/1.0 (progetto-scuola)'}


@trips_bp.route('/')
def index():
    if 'utente_id' not in session:
        return redirect(url_for('auth.login'))
    repo = TripRepository()
    viaggi = repo.get_all_by_user(session['utente_id'])
    return render_template('trips/index.html', viaggi=viaggi)


@trips_bp.route('/trips/new', methods=['GET', 'POST'])
def new():
    if 'utente_id' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        viaggio = Viaggio(
            utente_id=session['utente_id'],
            titolo=request.form['titolo'],
            data_inizio=request.form['data_inizio'],
            data_fine=request.form['data_fine'],
            note=request.form.get('note', '')
        )
        TripRepository().create(viaggio)
        return redirect(url_for('trips.index'))
    return render_template('trips/form.html', viaggio=None)


@trips_bp.route('/trips/<int:trip_id>')
def detail(trip_id):
    if 'utente_id' not in session:
        return redirect(url_for('auth.login'))
    viaggio = TripRepository().get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)
    destinazioni = DestinationRepository().get_by_trip(trip_id)
    return render_template('trips/detail.html', viaggio=viaggio, destinazioni=destinazioni)


@trips_bp.route('/trips/<int:trip_id>/edit', methods=['GET', 'POST'])
def edit(trip_id):
    if 'utente_id' not in session:
        return redirect(url_for('auth.login'))
    repo = TripRepository()
    viaggio = repo.get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)
    if request.method == 'POST':
        viaggio.titolo = request.form['titolo']
        viaggio.data_inizio = request.form['data_inizio']
        viaggio.data_fine = request.form['data_fine']
        viaggio.note = request.form.get('note', '')
        repo.update(viaggio)
        return redirect(url_for('trips.detail', trip_id=trip_id))
    return render_template('trips/form.html', viaggio=viaggio)


@trips_bp.route('/trips/<int:trip_id>/delete', methods=['POST'])
def delete(trip_id):
    if 'utente_id' not in session:
        return redirect(url_for('auth.login'))
    repo = TripRepository()
    viaggio = repo.get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)
    repo.delete(trip_id)
    return redirect(url_for('trips.index'))


@trips_bp.route('/trips/<int:trip_id>/destinazioni/add', methods=['GET', 'POST'])
def add_destination(trip_id):
    if 'utente_id' not in session:
        return redirect(url_for('auth.login'))
    viaggio = TripRepository().get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)

    risultati = []
    query = ''

    if request.method == 'POST':
        azione = request.form.get('azione')

        # Primo step: cerca la citta tramite Nominatim
        if azione == 'cerca':
            query = request.form.get('query', '')
            resp = requests.get(NOMINATIM_URL, params={
                'q': query, 'format': 'json', 'limit': 5
            }, headers=HEADERS, timeout=5)
            risultati = resp.json()
            return render_template('trips/add_destination.html',
                                   viaggio=viaggio, risultati=risultati, query=query)

        # Secondo step: conferma la destinazione selezionata
        if azione == 'conferma':
            dest = Destinazione(
                viaggio_id=trip_id,
                nome=request.form['nome'],
                lat=float(request.form['lat']),
                lng=float(request.form['lng'])
            )
            DestinationRepository().add(dest)
            return redirect(url_for('trips.detail', trip_id=trip_id))

    return render_template('trips/add_destination.html',
                           viaggio=viaggio, risultati=[], query='')


@trips_bp.route('/trips/<int:trip_id>/destinazioni/<int:dest_id>/delete', methods=['POST'])
def delete_destination(trip_id, dest_id):
    if 'utente_id' not in session:
        return redirect(url_for('auth.login'))
    viaggio = TripRepository().get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)
    DestinationRepository().delete(dest_id)
    return redirect(url_for('trips.detail', trip_id=trip_id))
