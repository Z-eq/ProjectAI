# Project AI Beskrivning
## Innehållsförteckning -
 [Översikt av filer](#översikt-av-filer) - [Databasfunktioner](#databasfunktioner) - [Databasstruktur och relationer](#databasstruktur-och-relationer) - [Rollback-funktion](#rollback-funktion) - [API-dokumentation](#api-dokumentation)

## Översikt av filer

### `app.py`
- Huvudfilen för att starta Flask-server appen att rendera html sidor
- Registrerar blueprint för olika delar av applikationen.
- Säkerställer att nödvändiga mappar och databaser finns.
-   Startar serven på host `0.0.0.0` och port `5000`. eller frivilligt port   som är ledig

### `file_query/routes.py`
- Hanterar frågor om filer.
- Kan lista, räkna och läsa filer beroende på användarens fråga.
- Använder OpenAI för att tolka frågor och ge svar.

### `web_generator/web_routes.py`
- Hanterar generering, uppdatering och rollback av webbsidor.
- Använder OpenAI för att skapa och uppdatera webbsidor baserat på användarens beskrivningar eller valda mallar i .json format.

### `utils.py`
- Innehåller funktioner för att initialisera databaser.
- Funktioner för att spara och hämta versioner av webbsidor.
- Funktion för att kommunicera med OpenAI API.

### `file_indexer.py`
- Innehåller funktioner för att extrahera text från olika filtyper.
- Funktioner för att indexera filer och spara deras innehåll i databasen.
- Funktioner för att hämta innehållet i specifika filer.


## Databasfunktioner

### Databasstruktur och relatione

Projektet använder SQLite, en enkel databas för att lagra information om filer och versioner av webbsidor.
 Det finns två databaser en för Fil förfrågningar och en för webgenerator.

### `file_index.db` ( filförfrågningar )
- Hanterar information om indexerade filer för file_query
- Tabell: `files`
  - **file_path**: TEXT (Primärnyckel) - Filens sökväg.
  - **content**: TEXT - Filens innehåll.

```sql
CREATE TABLE IF NOT EXISTS files (
    file_path TEXT PRIMARY KEY,
    content TEXT
);

```
#### Funktioner relaterade till `file_index.db`:

```py
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
    conn.close()` 

```
