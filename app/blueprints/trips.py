from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, abort, flash

from app.models import Viaggio, Destinazione, Attivita
from app.repositories.trip_repository import TripRepository
from app.repositories.destination_repository import DestinationRepository
from app.repositories.attivita_repository import AttivitaRepository

trips_bp = Blueprint('trips', __name__)

# Etichette e colori per i tipi di attivita (usati nel template)
TIPI_ATTIVITA = {
    'hotel':      {'label': 'H', 'nome': 'Hotel'},
    'ristorante': {'label': 'R', 'nome': 'Ristorante'},
    'museo':      {'label': 'M', 'nome': 'Museo'},
    'attrazione': {'label': 'A', 'nome': 'Attrazione'},
    'trasporto':  {'label': 'T', 'nome': 'Trasporto'},
    'generale':   {'label': 'G', 'nome': 'Generale'},
}


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'utente_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper


@trips_bp.route('/')
def index():
    viaggi = []
    if 'utente_id' in session:
        viaggi = TripRepository().get_all_by_user(session['utente_id'])
    return render_template('trips/index.html', viaggi=viaggi)


@trips_bp.route('/trips/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        data_inizio = request.form.get('data_inizio', '')
        data_fine = request.form.get('data_fine', '')
        if data_fine and data_inizio and data_fine < data_inizio:
            flash('La data di fine non puo essere precedente alla data di inizio.')
            return render_template('trips/form.html', viaggio=None)
        viaggio = Viaggio(
            utente_id=session['utente_id'],
            titolo=request.form['titolo'],
            data_inizio=data_inizio,
            data_fine=data_fine,
            note=request.form.get('note', '')
        )
        TripRepository().create(viaggio)
        return redirect(url_for('trips.index'))
    return render_template('trips/form.html', viaggio=None)


@trips_bp.route('/trips/<int:trip_id>')
@login_required
def detail(trip_id):
    viaggio = TripRepository().get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)

    destinazioni = DestinationRepository().get_by_trip(trip_id)
    att_repo = AttivitaRepository()

    # Costruisce la struttura dati completa per template e JS
    destinazioni_dati = []
    for d in destinazioni:
        attivita = att_repo.get_by_destination(d.id)
        destinazioni_dati.append({
            'id': d.id,
            'nome': d.nome,
            'lat': d.lat,
            'lng': d.lng,
            'data_arrivo': d.data_arrivo,
            'data_partenza': d.data_partenza,
            'attivita': [
                {'id': a.id, 'nome': a.nome, 'tipo': a.tipo}
                for a in attivita
            ]
        })

    return render_template('trips/detail.html',
                           viaggio=viaggio,
                           destinazioni=destinazioni,
                           destinazioni_dati=destinazioni_dati,
                           tipi_attivita=TIPI_ATTIVITA)


@trips_bp.route('/trips/<int:trip_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(trip_id):
    repo = TripRepository()
    viaggio = repo.get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)
    if request.method == 'POST':
        data_inizio = request.form.get('data_inizio', '')
        data_fine = request.form.get('data_fine', '')
        if data_fine and data_inizio and data_fine < data_inizio:
            flash('La data di fine non puo essere precedente alla data di inizio.')
            return render_template('trips/form.html', viaggio=viaggio)
        viaggio.titolo = request.form['titolo']
        viaggio.data_inizio = data_inizio
        viaggio.data_fine = data_fine
        viaggio.note = request.form.get('note', '')
        repo.update(viaggio)
        return redirect(url_for('trips.detail', trip_id=trip_id))
    return render_template('trips/form.html', viaggio=viaggio)


@trips_bp.route('/trips/<int:trip_id>/delete', methods=['POST'])
@login_required
def delete(trip_id):
    repo = TripRepository()
    viaggio = repo.get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)
    repo.delete(trip_id)
    return redirect(url_for('trips.index'))


@trips_bp.route('/trips/<int:trip_id>/destinazioni/add', methods=['POST'])
@login_required
def add_destination(trip_id):
    viaggio = TripRepository().get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)
    lat = request.form.get('lat') or None
    lng = request.form.get('lng') or None
    dest = Destinazione(
        viaggio_id=trip_id,
        nome=request.form['nome'],
        lat=float(lat) if lat else None,
        lng=float(lng) if lng else None,
        data_arrivo=request.form.get('data_arrivo') or None,
        data_partenza=request.form.get('data_partenza') or None,
    )
    DestinationRepository().add(dest)
    next_url = request.form.get('next') or url_for('trips.detail', trip_id=trip_id)
    return redirect(next_url)


@trips_bp.route('/trips/<int:trip_id>/destinazioni/<int:dest_id>/delete', methods=['POST'])
@login_required
def delete_destination(trip_id, dest_id):
    viaggio = TripRepository().get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)
    DestinationRepository().delete(dest_id)
    return redirect(url_for('trips.detail', trip_id=trip_id))


@trips_bp.route('/trips/<int:trip_id>/destinazioni/<int:dest_id>/attivita/add', methods=['POST'])
@login_required
def add_activity(trip_id, dest_id):
    viaggio = TripRepository().get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)
    att = Attivita(
        destinazione_id=dest_id,
        nome=request.form['nome'],
        tipo=request.form.get('tipo', 'generale')
    )
    AttivitaRepository().add(att)
    return redirect(url_for('trips.detail', trip_id=trip_id))


@trips_bp.route('/trips/<int:trip_id>/destinazioni/<int:dest_id>/attivita/<int:att_id>/delete',
                methods=['POST'])
@login_required
def delete_activity(trip_id, dest_id, att_id):
    viaggio = TripRepository().get_by_id(trip_id)
    if not viaggio or viaggio.utente_id != session['utente_id']:
        abort(403)
    AttivitaRepository().delete(att_id)
    return redirect(url_for('trips.detail', trip_id=trip_id))
