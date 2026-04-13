from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.blueprints.auth import auth_bp
    from app.blueprints.trips import trips_bp
    from app.blueprints.explore import explore_bp
    from app.blueprints.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(explore_bp)
    app.register_blueprint(api_bp)

    return app
