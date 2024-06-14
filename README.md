
# ProjectAI

## Översikt av filer

### `app.py`
- Huvudfilen för att starta Flask-appen.
- Registrerar blueprint för olika delar av applikationen.
- Säkerställer att nödvändiga mappar och databaser finns.

### `file_query/routes.py`
- Hanterar frågor om filer.
- Kan lista, räkna och läsa filer beroende på användarens fråga.
- Använder OpenAI för att tolka frågor och ge svar.

### `web_generator/web_routes.py`
- Hanterar generering, uppdatering och rollback av webbsidor.
- Använder OpenAI för att skapa och uppdatera webbsidor baserat på användarens beskrivningar eller valda mallar.

### `utils.py`
- Innehåller funktioner för att initialisera databaser.
- Funktioner för att spara och hämta versioner av webbsidor.
- Funktion för att kommunicera med OpenAI API.

### `file_indexer.py`
- Innehåller funktioner för att extrahera text från olika filtyper.
- Funktioner för att indexera filer och spara deras innehåll i databasen.
- Funktioner för att hämta innehållet i specifika filer.

## Databasfunktioner

### Databasstruktur och relationer

Projektet använder SQLite, en enkel databas för att lagra information om filer och versioner av webbsidor. Det finns två databaser:

### `file_index.db`
- Hanterar information om indexerade filer.
- Tabell: `files`
  - **file_path**: TEXT (Primärnyckel) - Filens sökväg.
  - **content**: TEXT - Filens innehåll.

```sql
CREATE TABLE IF NOT EXISTS files (
    file_path TEXT PRIMARY KEY,
    content TEXT
);

```python
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
python
Kopiera kod

Så här ser det ut korrekt formaterat i markdown:

```markdown
```python
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
