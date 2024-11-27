from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
CORS(app)

# Import des routes après l'initialisation de l'app pour éviter les imports circulaires
from routes import *

if __name__ == '__main__':
    with app.app_context():
        # Création des tables dans la base de données
        db.create_all()
    app.run(debug=True)
