import os
import openai
import logging
import sqlite3
from datetime import datetime
import time

# Initiera OpenAI API-nyckel
openai.api_key = os.getenv('OPENAI_API_KEY')
VERSIONS_DB = 'file_index.db'

# Funktion för att skicka en fråga till OpenAI och få ett svar
def query_openai_gpt(prompt):
    try:
        start_time = time.time()  # Starta tidtagning
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        end_time = time.time()  # Stoppa tidtagning
        elapsed_time = end_time - start_time
        logging.info(f"OpenAI API response time: {elapsed_time} seconds")
        
        content = response.choices[0].message['content'].strip()
        logging.info(f"Received response: {content}")
        
        # Extrahera bara HTML-innehållet om det är inneslutet i en kodblock
        if "```html" in content and "```" in content:
            start = content.find("```html") + len("```html")
            end = content.find("```", start)
            content = content[start:end].strip()
        
        return content
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return "There was an error processing your request. Please try again later."

# Funktion för att initiera databasen (skapa tabeller om de inte finns)
def initialize_db():
    conn = sqlite3.connect(VERSIONS_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            file_path TEXT PRIMARY KEY,
            content TEXT
        )
    ''')
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

# Funktion för att spara en version av en genererad webbsida
def save_version(page_name, content):
    conn = sqlite3.connect(VERSIONS_DB)
    cursor = conn.cursor()
    start_time = time.time()  # Starta tidtagning
    cursor.execute('''
        INSERT INTO web_generator_versions (page_name, timestamp, content)
        VALUES (?, ?, ?)
    ''', (page_name, datetime.now().isoformat(), content))
    conn.commit()
    end_time = time.time()  # Stoppa tidtagning
    elapsed_time = end_time - start_time
    logging.info(f"Saving version for {page_name} took {elapsed_time} seconds")
    conn.close()

# Funktion för att hämta alla versioner av genererade webbsidor
def get_versions():
    conn = sqlite3.connect(VERSIONS_DB)
    cursor = conn.cursor()
    start_time = time.time()  # Starta tidtagning
    cursor.execute('SELECT id, page_name, timestamp FROM web_generator_versions ORDER BY timestamp DESC')
    versions = cursor.fetchall()
    end_time = time.time()  # Stoppa tidtagning
    elapsed_time = end_time - start_time
    logging.info(f"Fetching all versions took {elapsed_time} seconds")
    conn.close()
    return versions

# Funktion för att hämta innehållet i en specifik version av en genererad webbsida
def get_version_by_id(version_id):
    conn = sqlite3.connect(VERSIONS_DB)
    cursor = conn.cursor()
    start_time = time.time()  # Starta tidtagning
    cursor.execute('SELECT content FROM web_generator_versions WHERE id = ?', (version_id,))
    version = cursor.fetchone()
    end_time = time.time()  # Stoppa tidtagning
    elapsed_time = end_time - start_time
    logging.info(f"Fetching version by ID {version_id} took {elapsed_time} seconds")
    conn.close()
    return version[0] if version else None
