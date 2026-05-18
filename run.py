from app import create_app
from dotenv import load_dotenv # Importa la libreria

# Carica le variabili dal file .env
load_dotenv()
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
