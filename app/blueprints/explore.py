from flask import Blueprint, render_template, session, request
from app.repositories.trip_repository import TripRepository

explore_bp = Blueprint('explore', __name__)


@explore_bp.route('/explore')
def search():
    # Accessibile anche senza login
    # Se l'utente e autenticato, passa la lista dei suoi viaggi
    # per permettergli di aggiungere la citta corrente a un viaggio
    viaggi = []
    if 'utente_id' in session:
        viaggi = TripRepository().get_all_by_user(session['utente_id'])
    return render_template('explore/search.html', viaggi=viaggi)
