# Project AI Description
Introduction
This project is aimed at developing an application that uses the OpenAI API to generate web pages, update web pages, and analyze files on your computer. The project is partially built with the help of ChatGPT. We have used code from already created projects and then modified it according to our needs. The project is far from complete and there is much to be done, but this is an overview of OpenAI API so far.

## Table of Contents
[Installation Instructions](InstallManual.md) - [File Overview](#file-overview) - [Database Functions](#database-functions) - [Database Structure and Relationships](#database-structure-and-relationships) - [Rollback Function](#rollback-function) - [API Documentation](#api-documentation) - [Flow Chart](FlowChart-ProjectAI.pdf)

## File Overview

### `app.py`
- Main file for starting the Flask server application to render HTML pages.
- Registers blueprints for different parts of the application.
- Ensures necessary folders and databases exist.
- Starts the server on host `0.0.0.0` and port `5000`, or optionally any available port.

### `file_query/routes.py`
- Handles file queries.
- Can list, count, and read files depending on the user's query.
- Uses OpenAI to interpret questions and provide answers.

### `web_generator/web_routes.py`
- Handles generation, updating, and rollback of web pages.
- Uses OpenAI to create and update web pages based on user descriptions or selected templates in JSON format.

### `utils.py`
- Contains functions to initialize databases.
- Functions to save and retrieve versions of web pages.
- Function to communicate with OpenAI API.

### `file_indexer.py`
- Contains functions to extract text from various file types.
- Functions to index files and save their contents in the database.
- Functions to retrieve the content of specific files.

## Database Functions

### Database Structure and Relationships

The project uses SQLite, a simple database to store information about files and versions of web pages. There are two databases: one for file queries and one for web generation.

### `file_index.db` (file queries)
- Manages information about indexed files for file_query.
- Table: `files`
  - **file_path**: TEXT (Primary Key) - File path.
  - **content**: TEXT - File content.
```sql
CREATE TABLE IF NOT EXISTS files (
    file_path TEXT PRIMARY KEY,
    content TEXT
);

```
#### Functions related to ´file_index.db´:


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
### `versions.db`( for web_generator )

-   Manages versions of generated web pages by inserting them into a table and subcolumns as described below. These are present in ´utils.py´.  

-   Tabell: `web_generator_versions`
    -   **id**: INTEGER (Primary Key, autoincrement) - Version ID.
    -   **page_name**: TEXT - The name of the web page as specified during creation and updates.
    -   **version_id**: TEXT - Unique ID for each version.
    -   **timestamp**: TEXT - TEXT - Timestamp when the version was created.
    -   **content**: TEXT - Content of the web page.

```sql
CREATE TABLE IF NOT EXISTS web_generator_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_name TEXT,
    version_id TEXT,
    timestamp TEXT,
    content TEXT
);
```

#### Functions related to `versions.db`:

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
## Rollback-function 

The rollback function is used to restore a web page to a previous version to ensure that you always have a backup if you make a mistake or change your mind. Here is an explanation of how it works:

1. The user selects a previous version of a web page.
2. The system retrieves the content for that version from the database.
3. The content is written back to the current file, restoring the page to the previous version.

### Code Example for rollback:

#### POST /web_generator/rollback


-   **Description**: Restores a web page to a previous version.
.
-   **Parameters**:
    -   `page_id`: ID of the page to be restored.
    -   `version_id`: ID of the version to be restored.


* ##### Functions are located in /web_generator/web_routes.py
 

```py
@web_generator_bp.route('/rollback', methods=['POST'])
def rollback():
    version_id = request.form['version_id']  # Get version ID from form
    page_name = request.form['page_name']  # Get page name from form
    
    logging.debug(f"Rollback requested for version_id: {version_id}, page_name: {page_name}")
    
    version_response = get_version_by_id(version_id)  # Get content for the specific version
    if version_response:
        try:
            file_path = os.path.join(OUTPUT_FOLDER_PATH, page_name, f"{page_name}.html")  # Get file path
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(version_response)  # Write version content to file
            
            flash('Rollback successful.', 'success')  # Display message that rollback was successful
            page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
            return render_template('web_generator.html', rollback_response=f'Rollback successful. <a href="{page_url}" target="_blank">View rolled back page</a>', versions=get_versions())
        except Exception as e:
            logging.error(f"Error during rollback: {e}")
            return render_template('web_generator.html', rollback_response="There was an error during rollback.", versions=get_versions())
    else:
        flash('Rollback failed. Version not found.', 'danger')  # Display error message if version not found
        return render_template('web_generator.html', rollback_response="Rollback failed. Version not found.", versions=get_versions())
 ``` 

## API-documentation

### OpenAI Query Function

*  Function to send queries to OpenAI and receive a response
* ( located in utils.py )

```python
def query_openai_gpt(prompt):
    try:
        # Send a query to OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert assistant that helps users with file queries and web page generation."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the response from OpenAI
        content = response.choices[0].message['content'].strip()
        logging.info(f"Received response: {content}")
        
        # Extract only HTML content if it is enclosed in a code block
        if "```html" in content and "```" in content:
            start = content.find("```html") + len("```html")
            end = content.find("```", start)
            content = content[start:end].strip()
        
        return content
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return "There was an error processing your request. Please try again later."
````

#### *  ( (API Examples below that are not included in the code but can be implemented, shown here for educational purposes!)

In the example below, we see the System's role and User's role. Additional user roles or changes to the System's role can be added, see more examples.

* Here we have prepared the system to be a customer service representative and allowed the user to ask freely without defining the prompt to something specific.. 
```py
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a customer service representative that helps users with their technical issues."},
        {"role": "user", "content": prompt}
    ]
)
````

- Below, we can use multi-step queries to specify more. In this example, we split the question into several steps to get a more structured answer.
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
Here, the system becomes a JSON expert and responds in JSON format. We can easily format a text file into JSON format.

```py
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assistant that provides JSON formatted responses."},
        {"role": "user", "content": prompt}
    ]
)
```
# API Endpoints and Examples

These examples demonstrate how to customize the use of the OpenAI API for various scenarios and needs. By altering roles, instructions, and formats, you can obtain responses better suited to specific use cases.

## API Endpoints

### GET /file_query
**Description:** Retrieves the `file_query.html` page.

### POST /file_query
**Description:** Handles file query requests.
**Parameters:**
- `query`: The question to be asked, e.g., "list files", "count files", "read file contents".
**Response:** Results based on the type of query.
- **List files:** Returns a list of file names.
- **Count files:** Returns the number of files.
- **Read file contents:** Returns the contents of the specified file.

#### Codexampple for /file_query:

```py
@file_query_bp.route('/file_query', methods=['GET', 'POST'])
def query_files():
    if request.method == 'POST':  # Check if the request is a POST
        user_query = request.form['query']  # Get the user's query
        read_files = 'read_files_toggle' in request.form  # Check if "read_files_toggle" is checked to read files.

        # Save toggle state in session
        session['read_files'] = read_files

        # Use OpenAI to determine the intent of the query
        intent_prompt = f"Determine the intent of this query: {user_query}. Possible intents include 'list file names', 'count files', 'read file contents', or 'general question'."
        intent_response = query_openai_gpt(intent_prompt).lower()

        folder_path = DEFAULT_FOLDER_PATH

        if 'list file names' in intent_response:  # Check if the intent is to list file names
            index_files(folder_path, read_content=False)  # Index files without reading content
            file_index = get_indexed_files(read_content=False)  # Get indexed files
            file_names = list(file_index)  # Convert to a list of file names to display in the browser
            return render_template('file_query.html', query=user_query, response=f"The files are: {', '.join(file_names)}")

        elif 'count files' in intent_response:  # Check if the intent is to count files
            index_files(folder_path, read_content=False)  # Index files without reading content
            file_index = get_indexed_files(read_content=False)  # Get indexed files
            file_count = len(file_index)  # Count the number of files
            return render_template('file_query.html', query=user_query, response=f"You have {file_count} files indexed.")

        elif 'read file contents' in intent_response:  # Check if the intent is to read file contents
            index_files(folder_path, read_content=True)  # Index files and read content
            file_index = get_indexed_files(read_content=True)  # Get indexed files with content
            # Extract file name from the query
            file_name = extract_file_name(user_query)
            file_path = os.path.join(folder_path, file_name)  # Get the file's path
            file_content = get_file_content(file_path)  # Get the file's content
            openai_prompt = f"Based on the content of the file {file_name}, answer the question: {user_query}\n\n{file_content}"
        else:  # If the query is general
            # General question, read files only if toggle is on
            if read_files:
                index_files(folder_path)  # Index and read files
                file_index = get_indexed_files()  # Get indexed files
                openai_prompt = f"You have permission to access and read the contents of the following files:\n{file_index}\nAnswer the question: {user_query}"
            else:
                openai_prompt = f"Answer the following question: {user_query}"

        # Ask OpenAI GPT-3.5 Turbo
        try:
            ai_response = query_openai_gpt(openai_prompt)  # Send the prompt to OpenAI and get a response
            formatted_response = ai_response.replace('\n', '<br>').replace('1. ', '<ol><li>').replace('2. ', '<li>').replace('3. ', '<li>').replace('4. ', '<li>').replace('5. ', '<li>').replace('6. ', '<li>').replace('7. ', '<li>').replace('8. ', '<li>').replace('9. ', '<li>') + '</li></ol>'  # Format the response for HTML
            return render_template('file_query.html', query=user_query, response=formatted_response)  # Display the response in HTML
        except Exception as e:  # If there is an error
            logging.error(f"Error processing query: {e}")  # Log the error
            return render_template('file_query.html', query=user_query, response="There was an error processing your request. Please try again later.")  # Display error message

    return render_template('file_query.html', read_files_toggle=session.get('read_files', False))  # Display the form with the current toggle state

def extract_file_name(query):
    # Use OpenAI to extract the file name from the query
    extraction_prompt = f"Extract the file name from the following query: {query}"
    file_name = query_openai_gpt(extraction_prompt).strip()  # Extract and clean the file name
    return file_name  # Return the file name
```

### GET /web_generator
-   **Description**: Retrieves the web_generator.html page.

### POST /web_generator

-   **Description**:  Description of how the web page should be. Must be very specific and detailed.
-   **Parameters**:
    -   `description`:  Description of how the web page should be. Must be very specific and detailed.
    -   
    -   `template`: Template to be used for the web page, in JSON format. Multiple templates can be added.
    -   
#### Codexample for /web_generator:

```py
@web_generator_bp.route('/web_generator', methods=['GET', 'POST'])
def generate_page():
    if request.method == 'POST':  # Check if the request is a POST
        page_name = request.form['page_name']  # Get the page name from the form
        page_description = request.form['page_description']  # Get the page description from the form
        template_choice = request.form.get('template_choice')  # Get the chosen template from the form

        logging.debug(f"Received page_name: {page_name}, page_description: {page_description}, template_choice: {template_choice}")

        if not page_name:  # If the page name is missing, display an error message
            flash('Page Name is required.', 'danger')
            return redirect(url_for('web_generator.generate_page'))

        page_folder_path = os.path.join(OUTPUT_FOLDER_PATH, page_name)  # Create a folder for the page
        os.makedirs(page_folder_path, exist_ok=True)  # Create the folder if it does not exist

        if page_description:  # If a page description is provided, use it to create the prompt
            openai_prompt = page_description
            html_content = query_openai_gpt(openai_prompt)  # Query OpenAI with the description
        elif template_choice in TEMPLATE_PROMPTS:  # If a template is chosen, use it
            html_content = query_openai_gpt(TEMPLATE_PROMPTS[template_choice])
        else:  # Otherwise, use a default template
            with open('default_template.json', 'r') as file:
                default_prompt = json.load(file)['prompt']
            html_content = query_openai_gpt(default_prompt)

        # Create the HTML template for the page
        html_template = f"""
        ........
        try:
            # Save the HTML file
            with open(os.path.join(page_folder_path, f"{page_name}.html"), 'w', encoding='utf-8') as file:
                file.write(html_template)
            # Save the CSS file 
            with open(os.path.join(page_folder_path, f"{page_name}.css"), 'w', encoding='utf-8') as file:
                file.write(css_content)
            # Save the JS file
            with open(os.path.join(page_folder_path, f"{page_name}.js"), 'w', encoding='utf-8') as file:
                file.write(js_content)

            # Save a version of the page
            save_version(page_name, html_template)
            page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
            return render_template('web_generator.html', generate_response=f'Webpage generated and saved to <a href="{page_url}" target="_blank">{page_name}.html</a>', versions=get_versions())
        except Exception as e:  # Handle any errors
            logging.error(f"Error saving files: {e}")
            return render_template('web_generator.html', generate_response="There was an error saving the generated files.", versions=get_versions())
    return render_template('web_generator.html', versions=get_versions())

````

### POST /web_generator/update

-   **Description**: Updates an existing web page. Parameters:

-  page_id: ID of the page to be updated.
-  content: New content for the page.

-  **Response:** Confirmation of the update.
- It is essential to be precise about what you request to update and to understand HTML code and naming conventions to ensure accuracy. There is still much room for improvement and optimization.


If u have questions feel free to conact me pm or mail zeq.alidemaj @ gmail.com
