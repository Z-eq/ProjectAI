# Project AI Beskrivning
Introduktion
Detta projekt är till att utveckla en applikation som använder OpenAI API för att generera websidor uppdatera websidor och analysera filer på egen dator. Projektet är delvis byggt med hjälp av ChatGPT, Vi har använt kod av redan skapade projekt och sedan gjort om till vår önskemål.
Långt ifrån klar projekt och myckt finns att göra men såjhär lånmgt får man se inblick av OpenAI API.
## Innehållsförteckning -
[Installations instruktioner](RAPPORT.md) - [Översikt av filer](#översikt-av-filer) - [Databasfunktioner](#databasfunktioner) - [Databasstruktur och relationer](#databasstruktur-och-relationer) -  [Rollback-funktion](#rollback-funktion) - [API-dokumentation](#api-dokumentation) -  [Flow Chart](FlowChart-ProjectAI.pdf)


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

### Databasstruktur och relationer

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
### `versions.db`( för web_generator )

-   Hantera versioner av genererade webbsidor genom att lägga in dem i tabell och undercolumner som nedan. Dessa finns i utils.py  

-   Tabell: `web_generator_versions`
    -   **id**: INTEGER (Primärnyckel, autoincrement) - Versions-ID.
    -   **page_name**: TEXT - Namnet på webbsidan man anger när man skapar det & uppdaterar.
    -   **version_id**: TEXT - Unikt ID för varje version.
    -   **timestamp**: TEXT - Tidpunkten då versionen skapades.
    -   **content**: TEXT - Innehållet i webbsidan.

```sql
CREATE TABLE IF NOT EXISTS web_generator_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_name TEXT,
    version_id TEXT,
    timestamp TEXT,
    content TEXT
);
```

#### Funktioner relaterade till `versions.db`:

```sql
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
    conn.close()` 
```
## Rollback-funktion 

Rollback-funktionen används för att återställa en webbsida till en tidigare version för att säkerställa att man alltid har en backup om man gjort fel eller ångrar sig. 
Här är en förklaring av hur den fungerar:

1.  Användaren väljer en tidigare version av en webbsida.
2.  Systemet hämtar innehållet för den versionen från databasen.
3.  Innehållet skrivs tillbaka till den aktuella filen, vilket återställer sidan till den tidigare versionen.

### Kodexempel för rollback:

#### POST /web_generator/rollback


-   **Beskrivning**: Återställer en webbsida till en tidigare version.
-   **Parametrar**:
    -   `page_id`: ID för sidan som ska återställas.
    -   `version_id`: ID för versionen som ska återställas.



* ##### Funktionerna finns i /web_generator/web_routes.py 

```py
@web_generator_bp.route('/rollback', methods=['POST'])
def rollback():
    version_id = request.form['version_id']  # Hämta versions-ID från formuläret
    page_name = request.form['page_name']  # Hämta sidnamnet från formuläret
    
    logging.debug(f"Rollback requested for version_id: {version_id}, page_name: {page_name}")
    
    version_response = get_version_by_id(version_id)  # Hämta innehållet för den specifika versionen
    if version_response:
        try:
            file_path = os.path.join(OUTPUT_FOLDER_PATH, page_name, f"{page_name}.html")  # Hämta filvägen
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(version_response)  # Skriv versionens innehåll till filen
            
            flash('Rollback successful.', 'success')  # Visa ett meddelande om att återställningen lyckades
            page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
            return render_template('web_generator.html', rollback_response=f'Rollback successful. <a href="{page_url}" target="_blank">View rolled back page</a>', versions=get_versions())
        except Exception as e:
            logging.error(f"Error during rollback: {e}")
            return render_template('web_generator.html', rollback_response="There was an error during rollback.", versions=get_versions())
    else:
        flash('Rollback failed. Version not found.', 'danger')  # Visa ett felmeddelande om versionen inte hittades
        return render_template('web_generator.html', rollback_response="Rollback failed. Version not found.", versions=get_versions())
 ``` 

## API-dokumentation

### OpenAI Query Funktion

*  Funktion för att skicka förfrågningar till OpenAI och få ett svar
* ( finns i utils.py )

```python
def query_openai_gpt(prompt):
    try:
        # Skickar en fråga till OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert assistant that helps users with file queries and web page generation."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extraherar svaret från OpenAI
        content = response.choices[0].message['content'].strip()
        logging.info(f"Received response: {content}")
        
        # Extraherar endast HTML-innehåll om det är inneslutet i en kodblock
        if "```html" in content and "```" in content:
            start = content.find("```html") + len("```html")
            end = content.find("```", start)
            content = content[start:end].strip()
        
        return content
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return "There was an error processing your request. Please try again later."
````

#### *  ( API Exempel nedaför som ej finns med i koden men som kan implementeras,  här visar  vi endast i lärosyfte! )

I exemplet nedan ser vi  Systemts roll och Användarens roll. Man kan lägga till flera användarroller eller ändra Systemts roll, se fler exempel. 

* Här har vi förberett systemet att bli en kundservice representant och låtit användaren fritt fråga frnom att inte definera : promt till något specifikt. 
```py
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a customer service representative that helps users with their technical issues."},
        {"role": "user", "content": prompt}
    ]
)
````

- Här nedan kan vi använda flerstegsfrågor för att specifiera mer. I detta exempel har vi delat frågan i flera steg för att få mer struktuerat svar.
```py
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an expert assistant that helps users with file queries and web page generation."},
        {"role": "user", "content": "I need help with generating a web page."},
        {"role": "assistant", "content": "Sure, what kind of web page do you need?"},
        {"role": "user", "content": "I need a landing page for my product."},
        {"role": "assistant", "content": "Got it. Do you have any specific requirements for the landing page?"},
        {"role": "user", "content": prompt}
    ]
)
```
Här blir systemet en json expert och svarar i json format. Vi kan lätt formatera en text fil till json fomrat. 
```py
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assistant that provides JSON formatted responses."},
        {"role": "user", "content": prompt}
    ]
)
```
Dessa exempel visar hur man kan anpassa användningen av OpenAI
API för olika scenarier och behov och genom att ändra på roller, instruktioner och format kan man få svar som är bättre anpassade till specifika användnings områden.


## API Endpoints

### GET /file_query

-   **Beskrivning**: Hämtar file_query.html sidan.

### POST /file_query

-   **Beskrivning**: Hanterar filfrågeförfrågningar.
-   **Parametrar**:
    -   `query`: Frågan som ska ställas ex (lista filer, räkna filer, läs filinnehåll).
-   **Svar**: Resultat baserat på frågetyp.
    -   Lista filer: Returnerar en lista med filnamn.
    -   Räkna filer: Returnerar antalet filer.
    -   Läs filinnehåll: Returnerar innehållet i specificerad fil.
    -  Kan begränsa API eller specifiera det att utföra något 
    - Kan lösa problem och utföra avancerade beräkningar baserat på egna materialet som finns i filerna.

#### Kodexempel för /file_query:

```py
@file_query_bp.route('/file_query', methods=['GET', 'POST'])
def query_files():
    if request.method == 'POST':  # Kolla om förfrågan är en POST
        user_query = request.form['query']  # Hämta användarens fråga
        read_files = 'read_files_toggle' in request.form  # Kolla om "read_files_toggle" är ikryssad för att kunna läsa filer.

        # Spara toggle state i session
        session['read_files'] = read_files

        # Använd OpenAI för att bestämma avsikten med frågan ( kan förfinas )
        intent_prompt = f"Determine the intent of this query: {user_query}. Possible intents include 'list file names', 'count files', 'read file contents', or 'general question'."
        intent_response = query_openai_gpt(intent_prompt).lower()

        folder_path = DEFAULT_FOLDER_PATH

        if 'list file names' in intent_response:  # Kolla om avsikten är att lista filnamn
            index_files(folder_path, read_content=False)  # Indexera filer utan att läsa innehåll (sparar tokens)
            file_index = get_indexed_files(read_content=False)  # Hämta indexerade filer (spara tokens)
            file_names = list(file_index)  # Konvertera till en lista med filnamn för att visa i webläsaren
            return render_template('file_query.html', query=user_query, response=f"The files are: {', '.join(file_names)}")

        elif 'count files' in intent_response:  # Kolla om avsikten är att räkna filer
            index_files(folder_path, read_content=False)  # Indexera filer utan att läsa innehåll
            file_index = get_indexed_files(read_content=False)  # Hämta indexerade filer
            file_count = len(file_index)  # Räkna antalet filer
            return render_template('file_query.html', query=user_query, response=f"You have {file_count} files indexed.")

        elif 'read file contents' in intent_response:  # Kolla om avsikten är att läsa filinnehåll
            index_files(folder_path, read_content=True)  # Indexera filer och läs innehåll
            file_index = get_indexed_files(read_content=True)  # Hämta indexerade filer med innehåll
            # Extrahera filnamn från frågan
            file_name = extract_file_name(user_query)
            file_path = os.path.join(folder_path, file_name)  # Hämta filens sökväg
            file_content = get_file_content(file_path)  # Hämta filens innehåll
            openai_prompt = f"Based on the content of the file {file_name}, answer the question: {user_query}\n\n{file_content}"
        else:  # Om frågan är allmän
            # Allmän fråga, läs filer endast om toggle är på
            if read_files:
                index_files(folder_path)  # Indexera och läs filer
                file_index = get_indexed_files()  # Hämta indexerade filer
                openai_prompt = f"You have permission to access and read the contents of the following files:\n{file_index}\nAnswer the question: {user_query}"
            else:
                openai_prompt = f"Answer the following question: {user_query}"

        # Fråga OpenAI GPT-3.5 Turbo
        try:
            ai_response = query_openai_gpt(openai_prompt)  # Skicka prompten till OpenAI och få svar
            formatted_response = ai_response.replace('\n', '<br>').replace('1. ', '<ol><li>').replace('2. ', '<li>').replace('3. ', '<li>').replace('4. ', '<li>').replace('5. ', '<li>').replace('6. ', '<li>').replace('7. ', '<li>').replace('8. ', '<li>').replace('9. ', '<li>') + '</li></ol>'  # Formatera svaret för HTML
            return render_template('file_query.html', query=user_query, response=formatted_response)  # Visa svaret i HTML
        except Exception as e:  # Om det blir ett fel
            logging.error(f"Error processing query: {e}")  # Logga felet
            return render_template('file_query.html', query=user_query, response="There was an error processing your request. Please try again later.")  # Visa felmeddelande

    return render_template('file_query.html', read_files_toggle=session.get('read_files', False))  # Visa formuläret med nuvarande toggle state

def extract_file_name(query):
    # Använd OpenAI för att extrahera filnamn från frågan
    extraction_prompt = f"Extract the file name from the following query: {query}"
    file_name = query_openai_gpt(extraction_prompt).strip()  # Extrahera och rensa filnamnet
    return file_name  # Returnera filnamnet
```

### GET /web_generator

-   **Beskrivning**: Hämtar webgenerator sidan web_generator.html.

### POST /web_generator

-   **Beskrivning**: Hanterar förfrågningar om att generera webbsidor.
-   **Parametrar**:
    -   `description`: Beskrivning för hur websidan ska vara, måste vara väldigt specifikt och detaljerat så möjlig.
    -   `template`: Mall som ska användas för webbsidan, innehåller redan för definerade promtar i .json format kan läggas till flera ( måste lägga till deras namn i html templates isåfall samt definera om web_routes.json till att använda andra format samt göra det anrop av filtyp.

#### Kodexempel för /web_generator:

```py
@web_generator_bp.route('/web_generator', methods=['GET', 'POST'])
def generate_page():
    if request.method == 'POST':  # Kolla att förfrågan är en POST
        page_name = request.form['page_name']  # Hämta sidnamnet från namn formen
        page_description = request.form['page_description']  # Hämta sidbeskrivningen från description formuläret
        template_choice = request.form.get('template_choice')  # Hämta vald mall från formuläret

        logging.debug(f"Received page_name: {page_name}, page_description: {page_description}, template_choice: {template_choice}")

        if not page_name:  # Om sidnamnet saknas, visa ett felmeddelande
            flash('Page Name is required.', 'danger')
            return redirect(url_for('web_generator.generate_page'))

        page_folder_path = os.path.join(OUTPUT_FOLDER_PATH, page_name)  # Skapa en mapp för sidan
        os.makedirs(page_folder_path, exist_ok=True)  # Skapa mappen om den inte finns

        if page_description:  # Om sidbeskrivning finns, använd den för att skapa prompten
            openai_prompt = page_description
            html_content = query_openai_gpt(openai_prompt)  # Fråga OpenAI med beskrivningen
        elif template_choice in TEMPLATE_PROMPTS:  # Om en mall är vald, använd den
            html_content = query_openai_gpt(TEMPLATE_PROMPTS[template_choice])
        else:  # Annars, använd en standardmall
            with open('default_template.json', 'r') as file:
                default_prompt = json.load(file)['prompt']
            html_content = query_openai_gpt(default_prompt)

        # Skapar HTML-mallen för sidan
        html_template = f"""
        ........
        try:
            # Spara HTML-filen i skrivläge
            with open(os.path.join(page_folder_path, f"{page_name}.html"), 'w', encoding='utf-8') as file:
                file.write(html_template)
            # Spara CSS-filen i skrivläge 
            with open(os.path.join(page_folder_path, f"{page_name}.css"), 'w', encoding='utf-8') as file:
                file.write(css_content)
            # Spara JS-filen i skrivläge
            with open(os.path.join(page_folder_path, f"{page_name}.js"), 'w', encoding='utf-8') as file:
                file.write(js_content)

            # Spara en version av sidan
            save_version(page_name, html_template)
            page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
            return render_template('web_generator.html', generate_response=f'Webpage generated and saved to <a href="{page_url}" target="_blank">{page_name}.html</a>', versions=get_versions())
        except Exception as e:  # Hantera eventuella fel
            logging.error(f"Error saving files: {e}")
            return render_template('web_generator.html', generate_response="There was an error saving the generated files.", versions=get_versions())
    return render_template('web_generator.html', versions=get_versions())
````

### POST /web_generator/update

-   **Beskrivning**: Uppdaterar en befintlig webbsida.
-   **Parametrar**:
    -   `page_id`: ID för sidan som ska uppdateras.
    -   `content`: Nytt innehåll för sidan.
-   **Svar**: Bekräftelse på uppdateringen.
- Man måste vara noga med vad man ber om att uppdatera och känna till html kod och benämningar föra att bli bra.. Finns mycket kvar att förbättra och effektisera!

#### Kodexempel för /web_generator/update:
```py
@web_generator_bp.route('/update_html', methods=['POST'])
def update_html():
    page_name = request.form['page_name']
    update_description = request.form['update_description']

    file_path = os.path.join(OUTPUT_FOLDER_PATH, page_name, f"{page_name}.html")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_content = file.read()
    except Exception as e:
        logging.error(f"Error reading HTML file: {e}")
        return render_template('web_generator.html', update_response="There was an error reading the HTML file.", versions=get_versions())

    openai_prompt = f"Here is the current HTML content:\n\n{existing_content}\n\nUpdate it based on the following description:\n\n{update_description}\n\nMake sure to only change the relevant sections and keep the rest of the content intact."
    updated_content = query_openai_gpt(openai_prompt)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        save_version(page_name, updated_content)
        page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
        return render_template('web_generator.html', update_response=f'HTML file updated successfully. <a href="{page_url}" target="_blank">View updated page</a>', versions=get_versions())
    except Exception as e:
        logging.error(f"Error updating HTML file: {e}")
        return render_template('web_generator.html', update_response="There was an error updating the HTML file.", versions=get_versions())
````


## Observationer

-   Implementeringen av filhantering var lite enklare men än mycket att lära sig, svårare var web generering var utmanande att göra rätt från början, alla detaljer måste vara uträknade och planerade och man bör kunna html eller noga inspektera genererade koden för att få rätt uppdatering då man måste unna benämningar. 
    
-   Filförfrågning kan bli fel ibland beroende på vad man frågar i början. Finns mycket kvar att kalibrera.
    
-   Att även använda sklearn modulen hade varit ett bra sätt att göra skriptet självlärande
    
-   Använda GPT-4-Turbo kan bidra till mer avancerad och nograre apimen dyrare!
    
-   Måste vara väldigt noga med koden så att man inte slösar token om man råkar ha en loop där stora filer finns.
    

## Slutsats

Tanken var endast vi skulle bygga en web generator men när vi insåg att man även skulle ha fil funktion för att man ska kunna spara/uppdatera websidor tyckte vi det var intressant att ha en fil assistent. Efter att ha testat vår egna fil assistent och webgenerator kan vi bara konstantera att OpenAI API är något man verkligen ska lära sig om man vill hänga med AI trenden och spara tid. Det går att göra mycket mer med API än med det vanliga chattbaserade boten.

ChatGPT kan även vara en stor vilseledare om man inte känner till lite grund programmering. Vi är övertygade om att AI är ny tidens Industrialisering och för dem som gillar teknik är detta en dröm som man än inte fattat har blivit verklighet och för dem som är oroliga att AI ska ta deras jobb vill vi avsluta med en citat som ej vem 

> "AI May Not Take Your Job, But Someone Using AI Likely Will"  
> — Richard Baldwin, an economist and professor
