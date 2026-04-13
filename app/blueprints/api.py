# Il blueprint api non e piu necessario: tutte le chiamate
# alle API esterne avvengono direttamente nei blueprint
# trips.py ed explore.py lato server.
# Il file viene mantenuto vuoto per compatibilita con la struttura.

from flask import Blueprint

api_bp = Blueprint('api', __name__)
