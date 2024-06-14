
Projektbeskrivning på enkel svenska
Översikt av filer
app.py

Huvudfilen för att starta Flask-appen.
Registrerar blueprint för olika delar av applikationen.
Säkerställer att nödvändiga mappar och databaser finns.
file_query/routes.py

Hanterar frågor om filer.
Kan lista, räkna och läsa filer beroende på användarens fråga.
Använder OpenAI för att tolka frågor och ge svar.
web_generator/web_routes.py

Hanterar generering, uppdatering och rollback av webbsidor.
Använder OpenAI för att skapa och uppdatera webbsidor baserat på användarens beskrivningar eller valda mallar.
utils.py

Innehåller funktioner för att initialisera databaser.
Funktioner för att spara och hämta versioner av webbsidor.
Funktion för att kommunicera med OpenAI API.
file_indexer.py

Innehåller funktioner för att extrahera text från olika filtyper.
Funktioner för att indexera filer och spara deras innehåll i databasen.
Funktioner för att hämta innehållet i specifika filer.
Databasfunktioner
Databasstruktur och relationer
Projektet använder SQLite, en enkel databas för att lagra information om filer och versioner av webbsidor. Det finns två databaser:

file_index.db

Hanterar information om indexerade filer.
Tabell: files
file_path: TEXT (Primärnyckel) - Filens sökväg.
content: TEXT - Filens innehåll.
sql
Kopiera kod
CREATE TABLE IF NOT EXISTS files (
    file_path TEXT PRIMARY KEY,
    content TEXT
);
Funktioner relaterade till file_index.db:

python
Kopiera kod
def initialize_file_index_db():
    conn = sqlite3.connect(FILE_INDEX_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            file_path TEXT PRIMARY KEY,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()
versions.db

Hanterar versioner av genererade webbsidor.
Tabell: web_generator_versions
id: INTEGER (Primärnyckel, autoincrement) - Versions-ID.
page_name: TEXT - Namnet på webbsidan.
version_id: TEXT - Unikt ID för varje version.
timestamp: TEXT - Tidpunkten då versionen skapades.
content: TEXT - Innehållet i webbsidan.
sql
Kopiera kod
CREATE TABLE IF NOT EXISTS web_generator_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_name TEXT,
    version_id TEXT,
    timestamp TEXT,
    content TEXT
);
Funktioner relaterade till versions.db:

python
Kopiera kod
def initialize_versions_db():
    conn = sqlite3.connect(VERSIONS_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS web_generator_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_name TEXT,
            version_id TEXT,
            timestamp TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()
Rollback-funktion
Rollback-funktionen används för att återställa en webbsida till en tidigare version. Här är en förklaring av hur den fungerar:

Användaren väljer en tidigare version av en webbsida.
Systemet hämtar innehållet för den versionen från databasen.
Innehållet skrivs tillbaka till den aktuella filen, vilket återställer sidan till den tidigare versionen.
Kodexempel för rollback:

python
Kopiera kod
@web_generator_bp.route('/rollback', methods=['POST'])
def rollback():
    version_id = request.form['version_id']
    page_name = request.form['page_name']
    
    logging.debug(f"Rollback requested for version_id: {version_id}, page_name: {page_name}")
    
    version_response = get_version_by_id(version_id)
    if version_response:
        try:
            file_path = os.path.join(OUTPUT_FOLDER_PATH, page_name, f"{page_name}.html")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(version_response)
            
            flash('Rollback successful.', 'success')
            page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
            return render_template('web_generator.html', rollback_response=f'Rollback successful. <a href="{page_url}" target="_blank">View rolled back page</a>', versions=get_versions())
        except Exception as e:
            logging.error(f"Error during rollback: {e}")
            return render_template('web_generator.html', rollback_response="There was an error during rollback.", versions=get_versions())
    else:
        flash('Rollback failed. Version not found.', 'danger')
        return render_template('web_generator.html', rollback_response="Rollback failed. Version
