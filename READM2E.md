
# Databasanvändning och relationer i projektet

Projektet använder SQLite, en inbäddad SQL-databas, för att lagra information om filer och versioner av genererade webbsidor. Det finns två huvudsakliga databaser som hanteras i detta projekt:

- **file_index.db**: Hanterar information om indexerade filer.
- **versions.db**: Hanterar versioner av genererade webbsidor.

## file_index.db

Denna databas hanterar indexeringen av filer. Databasen har en tabell som heter `files`.

### Tabell: files

- `file_path`: TEXT (Primärnyckel) - Filens sökväg.
- `content`: TEXT - Filens innehåll.

### Exempel på SQL-schema:

``sql
CREATE TABLE IF NOT EXISTS files (
    file_path TEXT PRIMARY KEY,
    content TEXT
);

 
 ### Funktioner relaterade till file_index.db: `
initialize_file_index_db: Initierar databasen genom att skapa tabellen om den inte redan finns.
index_files: Indexerar filer i en given mapp och sparar deras innehåll i databasen.
get_indexed_files: Hämtar alla indexerade filer, antingen med eller utan innehåll.
get_file_content: Hämtar innehållet i en specifik fil baserat på dess sökväg.
versions.db
Denna databas hanterar versionerna av genererade webbsidor. Databasen har en tabell som heter web_generator_versions.

Tabell: web_generator_versions
id: INTEGER (Primärnyckel, autoincrement) - Versions-ID.
page_name: TEXT - Namnet på webbsidan.
timestamp: TEXT - Tidpunkten då versionen skapades.
content: TEXT - Innehållet i webbsidan.
Exempel på SQL-schema:
sql
Kopiera kod
CREATE TABLE IF NOT EXISTS web_generator_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_name TEXT,
    timestamp TEXT,
    content TEXT
);
Funktioner relaterade till versions.db:
initialize_versions_db: Initierar databasen genom att skapa tabellen om den inte redan finns.
save_version: Sparar en version av en genererad webbsida.
get_versions: Hämtar alla versioner av genererade webbsidor.
get_version_by_id: Hämtar en specifik version baserat på dess ID.
Förklaring av funktioner och deras relation till databasen
1. initialize_file_index_db
Denna funktion ansluter till file_index.db och skapar tabellen files om den inte redan finns.

python
Kopiera kod
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
2. initialize_versions_db
Denna funktion ansluter till versions.db och skapar tabellen web_generator_versions om den inte redan finns.

python
Kopiera kod
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
3. index_files
Denna funktion indexerar filer i en given mapp och uppdaterar deras innehåll i file_index.db. Funktionen initialiserar databasen, ansluter till databasen, hämtar aktuella filer och uppdaterar tabellen files med filernas sökvägar och innehåll. Den tar också bort filer från databasen som inte längre finns i den givna mappen.

python
Kopiera kod
def index_files(folder_path, read_content=True):
    initialize_file_index_db()
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
4. save_version
Denna funktion sparar en version av en genererad webbsida i versions.db.

python
Kopiera kod
def save_version(page_name, content):
    conn = sqlite3.connect('versions.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO web_generator_versions (page_name, timestamp, content) VALUES (?, ?, ?)', (page_name, timestamp, content))
    conn.commit()
    conn.close()
Relationer mellan tabeller och funktioner
file_index.db och tabellen files används för att lagra och hantera filer och deras innehåll.
versions.db och tabellen web_generator_versions används för att spara och hantera versioner av genererade webbsidor.
Funktionerna som initialize_file_index_db, initialize_versions_db, index_files, och save_version ser till att dessa tabeller skapas, uppdateras och hanteras korrekt.
