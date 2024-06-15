### Python-skript:

-   `app.py`
-   `file_indexer.py`
-   `utils.py`

### Underkatalog för Filfrågor:

-   `file_query/routes.py`

### Underkatalog för Webbgenerator:

-   `web_generator/web_routes.py` 

### Mallfiler (HTML):

-   `templates/file_query.html`
-   `templates/index.html`
-   `templates/version_history.html`
-   `templates/web_generator.html`

### Mall för Promptfiler:

-   `default_template.json`
-   `template_prompts.json`

### `app.py`-filen startar en Flask-webbapplikation. Här är huvudpunkterna:

#### Importerar:

-   Standardbibliotek: `os` och `logging`
-   Flask-moduler: `Flask` och `render_template`
-   Anpassade moduler och blueprints: `file_query.routes`, `web_generator.web_routes` och `utils`

#### Flask Applikationsinställning:

-   Initierar Flask-appen.
-   Sätter en hemlig nyckel för sessionshantering.
-   Registrerar blueprints för modulär applikationsstruktur:
    -   `file_query_bp`
    -   `web_generator_bp`

#### Output Folder:

-   Säkerställer att en `OUTPUT_FOLDER_PATH` finns för att lagra genererade statiska filer.

#### Databasinitiering:

-   Anropar `initialize_file_index_db()` och `initialize_versions_db()` från `utils`-modulen för att ställa in nödvändiga databaser.

#### Loggning:

-   Konfigurerar loggning för felsökning.

#### Routes:

-   Definierar en route för startsidan som renderar `index.html`.

#### Kör Applikationen:

-   Kör Flask-appen i debug-läge på värd `0.0.0.0` och port `5002`.

----------

### `file_indexer.py`-filen ansvarar för att indexera filer och extrahera deras innehåll. Här är en översikt av dess funktionalitet:

#### Importerar:

-   Standardbibliotek: `os`, `sqlite3`, `mimetypes`
-   Tredjepartsbibliotek: `PyPDF2`, `pandas`, `BeautifulSoup`
-   Anpassad modul: `initialize_file_index_db` från `utils`

#### Extrahera Text Funktion (`extract_text`):

-   Bestämmer MIME-typen av en fil och extraherar text baserat på filtypen:
    -   PDF: Använder `PyPDF2` för att läsa text från varje sida.
    -   Excel: Använder `pandas` för att läsa innehållet och konvertera det till en sträng.
    -   Plain Text: Läser innehållet direkt.
    -   HTML: Använder `BeautifulSoup` för att parsa och extrahera text.
    -   Unsupported File Types: Returnerar ett meddelande som indikerar osupporterade filtyper.

#### Indexera Filer Funktion (`index_files`):

-   Initierar filindexdatabasen.
-   Ansluter till SQLite-databasen `file_index.db`.
-   Hämtar alla filer från den angivna mappen och identifierar deras sökvägar.
-   Jämför aktuella filer med de som redan finns i databasen.
-   Extraherar innehåll från nya eller uppdaterade filer och lagrar det i databasen.

----------

### `utils.py`-filen innehåller verktygsfunktioner och konfigurationer för projektet. Här är en sammanfattning av dess funktionalitet:

#### Importerar:

-   Standardbibliotek: `os`, `logging`, `sqlite3`, `datetime`
-   Tredjepartsbibliotek: `openai`

#### OpenAI API-initiering:

-   Sätter OpenAI API-nyckeln med en miljövariabel.

#### Konstanter:

-   `VERSIONS_DB`: Namn på versionsdatabasfilen.
-   `FILE_INDEX_DB`: Namn på filindexdatabasfilen.

#### Fråga OpenAI Funktion (`query_openai_gpt`):

-   Skickar en prompt till OpenAI
    
    GPT-3.5-turbo-modell.
-   Bearbetar svaret för att extrahera HTML-innehåll om det är inneslutet i en kodblock.
-   Loggar svarsinnehållet.
-   Hanterar eventuella API-fel och loggar dem.

#### Initiera Filindexdatabas (`initialize_file_index_db`):

-   Ansluter till SQLite-databasen `file_index.db`.
-   Skapar en `files`-tabell om den inte redan finns, med kolumner för `file_path` och `content`.
-   Commitar ändringar och stänger anslutningen.

#### Initiera Versionsdatabas (`initialize_versions_db`):

-   Ansluter till SQLite-databasen `versions.db`.
-   Skapar en `web_generator_versions`-tabell om den inte redan finns, med kolumner för `id`, `page_name`, `timestamp` och `content`.
-   Commitar ändringar och stänger anslutningen.

----------

### `web_generator/web_routes.py`-filen definierar routes och funktioner för att generera webbsidor. Här är en översikt:

#### Importerar:

-   Standardbibliotek: `os`, `logging`, `shutil`, `json`
-   Flask-moduler: `Blueprint`, `request`, `render_template`, `flash`, `redirect`, `url_for`
-   Anpassade verktyg: `query_openai_gpt`, `save_version`, `get_versions`, `get_version_by_id`
-   `datetime` för tidsstämpelhantering

#### Blueprint Setup:

-   Skapar en Blueprint för webbgeneratormodulen (`web_generator_bp`).

#### Output Folder:

-   Definierar `OUTPUT_FOLDER_PATH` för att lagra genererade webbsidor.

#### Mallprompter:

-   Laddar mallprompter från `template_prompts.json`.
-   `TEMPLATE_PROMPTS`-ordboken lagrar dessa prompter för senare användning.

#### Generera Sida Route (`/web_generator`):

-   Hanterar både GET och POST-förfrågningar.
-   Vid POST-förfrågan bearbetar den formulärdata för att generera en ny webbsida:
    -   Extraherar `page_name`, `page_description` och `template_choice` från formuläret.
    -   Validerar `page_name`.
    -   Skapar en katalog för den nya sidan under `OUTPUT_FOLDER_PATH`.
    -   Konstruerar en OpenAI-prompt baserat på den angivna `page_description` eller valda `template_choice`.
    -   Använder funktionen `query_openai_gpt` för att generera HTML-innehåll baserat på prompten.
    -   Sparar det genererade innehållet i lämplig mapp.

----------

### `index.html`-filen fungerar som huvudsidan för webbapplikationen. Här är de viktigaste elementen:

#### HTML-struktur:

-   Dokumentet följer standard HTML5-struktur med `<!DOCTYPE html>`, `<html>`, `<head>` och `<body>`-taggar.

#### Head-sektion:

-   Sätter teckenkodningen till UTF-8.
-   Inkluderar en titel: "Analyze and Generate".
-   Länkar till Bootstrap 4.5.2 CSS för styling.

#### Styles:

-   Definierar en anpassad stil för att centrera knappar med Flexbox.

#### Body-sektion:

-   Använder Bootstraps rutnätssystem för att skapa en centrerad behållare.
-   Visar en rubrik: "Main Page".
-   Tillhandahåller två knappar:
    -   "Go to File Query" som länkar till filfrågefunktionen.
    -   "Go to Web Generator" som länkar till webbsidagenereringsfunktionen.

----------

### Applikationen är strukturerad för att erbjuda två huvudfunktioner:

-   Filfrågor och indexering.
-   Webbsidagenerering med hjälp av prompter och mallar.
