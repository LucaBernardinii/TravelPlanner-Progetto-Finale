from flask import Flask
from config import Config
import os


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # MODIFICA QUI:
    # os.environ.get('NOME_VAR', 'valore_default')
    # Se trova SECRET_KEY nel sistema/file .env la usa.
    # Altrimenti usa 'dev' (utile per non bloccarci se manca il file).
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite'),
    )

    from app.blueprints.auth import auth_bp
    from app.blueprints.trips import trips_bp
    from app.blueprints.explore import explore_bp
    from app.blueprints.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(explore_bp)
    app.register_blueprint(api_bp)

    return app
