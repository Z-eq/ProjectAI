import os  # 
import logging  # 
from flask import Flask, render_template  # Flask används för att skapa webappen, render_template för att visa HTML-sidor
from file_query.routes import file_query_bp  # Importerar blueprint för filfrågor
from web_generator.web_routes import web_generator_bp  # Importerar blueprint för webbgeneratorn
from utils import initialize_file_index_db, initialize_versions_db  # Importerar funktioner för att initiera databaser

# Starta flaskserver app
app = Flask(__name__)
# Sätter en hemlig nyckel för sessionshantering som genereras slumpmässigt om den inte finns i os envoriment.
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())

# Registrerar blueprints
app.register_blueprint(file_query_bp)  # Registrerar blueprint för filförfrågningar file_query 
app.register_blueprint(web_generator_bp)  # Registrerar blueprint för webbgeneratorn

# Initialiserar databaser
initialize_file_index_db()  # Startar databasen för filindex
initialize_versions_db()  # Startar databasen för versioner

# Enkel loggning med lite extra info
logging.basicConfig(level=logging.DEBUG)  # Sätter loggning till DEBUG

# Definierar en rutt för huvudhemsidan
@app.route('/')
def home():
    return render_template('index.html')  # Visar index.html som hemsida

# Startar Flask-applikationen i debug-läge
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)  # Kör appen på port 5002 ( kan ändras till valfritt fri port)
