Projekt Namn
Översikt
Detta projekt är en webbapplikation som använder Flask för att hantera filförfrågningar och generera webbsidor. Applikationen använder SQLite-databaser för att lagra filinformation och versioner av genererade sidor.

Funktionalitet
Indexera och lagra filer
Hantera filförfrågningar (lista filer, räkna filer, läsa innehåll)
Generera och uppdatera webbsidor
Spara och återställa versioner av webbsidor
Installation
Klona repositoryn:
sh
Kopiera kod
git clone https://github.com/användare/projekt.git
Navigera till projektmappen:
sh
Kopiera kod
cd projekt
Installera nödvändiga paket:
sh
Kopiera kod
pip install -r requirements.txt
Starta applikationen:
sh
Kopiera kod
python app.py
Användning
Besök http://localhost:5002 i din webbläsare för att se startsidan.
Använd http://localhost:5002/file_query för att hantera filförfrågningar.
Använd http://localhost:5002/web_generator för att generera och uppdatera webbsidor.
Filstruktur och beskrivning
app.py
app.py är huvudfilen som startar Flask-applikationen. Den:

Skapar en Flask-applikation.
Initierar databaser.
Registrerar blueprints för att hantera olika delar av applikationen.
Startar Flask-servern.
utils.py
utils.py innehåller hjälpfunktioner för att initiera databaser och hantera databasoperationer:

initialize_file_index_db(): Initierar file_index.db genom att skapa tabellen files om den inte redan finns.
initialize_versions_db(): Initierar versions.db genom att skapa tabellen web_generator_versions om den inte redan finns.
file_query/routes.py
Denna fil innehåller rutter och logik för att hantera filförfrågningar:

GET /file_query: Visar formuläret för filförfrågningar.
POST /file_query: Hanterar filförfrågningar med hjälp av OpenAI API för att bestämma typ av förfrågan (lista filer, räkna filer, läsa filinnehåll).
web_generator/web_routes.py
Denna fil innehåller rutter och logik för att generera och uppdatera webbsidor:

GET /web_generator: Visar formuläret för att skapa webbsidor.
POST /web_generator: Hanterar skapandet av webbsidor med hjälp av OpenAI API.
POST /web_generator/update: Uppdaterar en befintlig webbsida.
POST /web_generator/rollback: Återställer en tidigare version av en webbsida.
file_indexer.py
Denna fil innehåller logik för att indexera filer och hantera deras innehåll:

index_files(): Indexerar filer i en given mapp.
get_indexed_files(): Hämtar alla indexerade filer.
get_file_content(): Hämtar innehållet i en specifik fil.
API Dokumentation
GET /file_query
Beskrivning: Hämta formuläret för filförfrågningar.
Respons: HTML-formulär för filförfrågningar.
POST /file_query
Beskrivning: Hantera filförfrågningar.
Parametrar:
query: Förfrågan som ska utföras (lista filer, räkna filer, läsa filinnehåll).
Respons: Resultat baserat på förfrågningstypen.
Lista filer: Returnerar en lista med filnamn.
Räkna filer: Returnerar antalet filer.
Läsa filinnehåll: Returnerar innehållet i den angivna filen.
Användning av OpenAI API
Beskrivning: Bestäm typ av filförfrågan med hjälp av OpenAI API.
Så här fungerar det:
Förfrågan från användaren skickas till OpenAI API.
OpenAI API analyserar förfrågan och returnerar typen (lista filer, räkna filer, läsa filinnehåll).
Baserat på svaret utförs lämplig åtgärd.
GET /web_generator
Beskrivning: Hämta formuläret för att skapa webbsidor.
Respons: HTML-formulär för att skapa webbsidor.
POST /web_generator
Beskrivning: Hantera förfrågningar för att skapa webbsidor.
Parametrar:
description: Beskrivning av webbsidan.
template: Mall som ska användas för webbsidan.
Respons: HTML-innehåll för den genererade webbsidan.
Användning av OpenAI API
Beskrivning: Generera HTML-innehåll för webbsidan med hjälp av OpenAI API.
Så här fungerar det:
Beskrivningen från användaren skickas till OpenAI API.
OpenAI API genererar HTML-innehåll baserat på beskrivningen.
Det genererade HTML-innehållet returneras och sparas som en ny webbsida.
POST /web_generator/update
Beskrivning: Uppdatera en befintlig webbsida.
Parametrar:
page_id: ID för sidan som ska uppdateras.
content: Nytt innehåll för sidan.
Respons: Bekräftelse på att uppdateringen har utförts.
POST /web_generator/rollback
Beskrivning: Återställ en tidigare version av en webbsida.
Parametrar:
page_id: ID för sidan som ska återställas.
version_id: ID för versionen som ska återställas.
Respons: Bekräftelse på att återställningen har utförts.
Användning av OpenAI API
Översikt
Projektet använder OpenAI API för att hantera naturlig språkbehandling. Här är en sammanfattning av hur det används:

Filförfrågningar
När en användare skickar en filförfrågan, analyserar OpenAI API förfrågan för att bestämma vilken typ av åtgärd som ska utföras (lista filer, räkna filer, läsa filinnehåll).
Generering av webbsidor
När en användare vill skapa en ny webbsida, skickas beskrivningen av sidan till OpenAI API, som genererar HTML-innehållet för sidan baserat på beskrivningen.
Källkodsförklaring
app.py
python
Kopiera kod
import os
import logging
from flask import Flask, render_template
from file_query.routes import file_query_bp
from web_generator.web_routes import web_generator_bp
from utils import initialize_file_index_db, initialize_versions_db

# Starta flaskserver app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())

# Initiera databaser
initialize_file_index_db()
initialize_versions_db()

# Registrera blueprints
app.register_blueprint(file_query_bp)
app.register_blueprint(web_generator_bp)

# Kolla om output-mappen finns, om inte, skapa den
OUTPUT_FOLDER_PATH = 'static/output'
os.makedirs(OUTPUT_FOLDER_PATH, exist_ok=True)

# Enkelt loggsystem med extra info
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')  # Visa startsidan

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)  # Starta appen i debug-läge
utils.py
python
Kopiera kod
import sqlite3

def initialize_file_index_db():
    conn = sqlite3.connect('file_index.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            file_path TEXT PRIMARY KEY,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def initialize_versions_db():
    conn = sqlite3.connect('versions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS web_generator_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_name TEXT,
            timestamp TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()
file_query/routes.py
python
Kopiera kod
from flask import Blueprint, request, render_template, jsonify
from utils import get_indexed_files, get_file_content, index_files
import openai

file_query_bp = Blueprint('file_query_bp', __name__)

@file_query_bp.route('/file_query', methods=['GET'])
def show_file_query_form():
    return render_template('file_query.html')

@file_query_bp.route('/file_query', methods=['POST'])
def handle_file_query():
    query = request.form.get('query')
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Identify the type of file query: {query}",
        max_tokens=5
    )
    query_type = response.choices[0].text.strip().lower()
    
    if 'list' in query_type:
        files = get_indexed_files()
        return jsonify(files)
    elif 'count' in query_type:
        files = get_indexed_files()
        return jsonify({"count": len(files)})
    elif 'read' in query_type:
        file_path = query.split('read ')[-1].strip()
        content = get_file_content(file_path)
        return jsonify({"content": content})
    else:
        return jsonify({"error": "Unknown query type"}), 400
web_generator/web_routes.py
python
Kopiera kod
from flask import Blueprint, request, render_template, jsonify
from datetime import datetime
import openai
import os

web_generator_bp = Blueprint('web_generator_bp', __name__)

@web_generator_bp.route('/web_generator', methods=['GET'])
def show_web_generator_form():
    return render_template('web_generator.html')

@web_generator_bp.route('/web_generator', methods=['POST'])
def generate_web_page():
    description = request.form.get('description')
    template = request.form.get('template')
    
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Generate HTML for a webpage with the following description: {description}",
        max_tokens=500
    )
    
    html_content = response.choices[0].text.strip()
    file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    file_path = os.path.join('static/output', file_name)
    
    with open(file_path, 'w') as f:
        f.write(html_content)
    
    return jsonify({"file_path": file_path})

@web_generator_bp.route('/web_generator/update', methods=['POST'])
def update_web_page():
    page_id = request.form.get('page_id')
    new_content = request.form.get('content')
    
    file_path = os.path.join('static/output', f"{page_id}.html")
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    return jsonify({"message": "Page updated successfully"})

@web_generator_bp.route('/web_generator/rollback', methods=['POST'])
def rollback_web_page():
    page_id = request.form.get('page_id')
    version_id = request.form.get('version_id')
    
    # Implement the logic to rollback to a previous version
    # This is just a placeholder implementation
    version_file_path = os.path.join('static/output', f"{version_id}.html")
    current_file_path = os.path.join('static/output', f"{page_id}.html")
    
    if os.path.exists(version_file_path):
        with open(version_file_path, 'r') as vf:
            content = vf.read()
        
        with open(current_file_path, 'w') as cf:
            cf.write(content)
        
        return jsonify({"message": "Rollback successful"})
    else:
        return jsonify({"error": "Version not found"}), 404
file_indexer.py
python
Kopiera kod
import os
import sqlite3

def index_files(folder_path, read_content=True):
    conn = sqlite3.connect('file_index.db')
    cursor = conn.cursor()
    
    current_files = {os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files}
    cursor.execute('SELECT file_path FROM files')
    db_files = {row[0] for row in cursor.fetchall()}
    
    for file_path in current_files:
        content = extract_text(file_path) if read_content else ""
        cursor.execute('REPLACE INTO files (file_path, content) VALUES (?, ?)', (file_path, content))
    
    for file_path in db_files - current_files:
        cursor.execute('DELETE FROM files WHERE file_path = ?', (file_path,))
    
    conn.commit()
    conn.close()

def get_indexed_files():
    conn = sqlite3.connect('file_index.db')
    cursor = conn.cursor()
    cursor.execute('SELECT file_path FROM files')
    files = cursor.fetchall()
    conn.close()
    return [file[0] for file in files]

def get_file_content(file_path):
    conn = sqlite3.connect('file_index.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM files WHERE file_path = ?', (file_path,))
    content = cursor.fetchone()
    conn.close()
    return content[0] if content else None

def extract_text(file_path):
    # Implement the logic to extract text content from a file
    # This is just a placeholder implementation
    with open(file_path, 'r') as file:
        return file.read()
Detta ger en komplett och detaljerad dokumentation av ditt projekt, inklusive installation, användning, API-dokumentation, källkodsförklaringar och beskrivningar av de olika .py-filerna.
