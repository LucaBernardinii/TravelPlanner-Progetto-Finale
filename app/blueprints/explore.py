from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, session

explore_bp = Blueprint('explore', __name__)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'utente_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper


@explore_bp.route('/explore')
@login_required
def search():
    # Tutta la logica e gestita lato client da explore.js
    # tramite le route /api/* del blueprint api
    return render_template('explore/search.html')
