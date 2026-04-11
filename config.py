import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'chiave-di-sviluppo-da-cambiare')
    DB_PATH = os.getenv('DB_PATH', 'instance/travel.sqlite')
