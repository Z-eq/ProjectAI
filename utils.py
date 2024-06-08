import os
import openai
import logging
import sqlite3
from datetime import datetime

# Initialize OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
FILE_INDEX_DB = 'file_index.db'
VERSIONS_DB = 'versions.db'

# Function to query OpenAI and get a response
def query_openai_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message['content'].strip()
        logging.info(f"Received response: {content}")
        
        # Extract only HTML content if enclosed within a code block
        if "```html" in content and "```" in content:
            start = content.find("```html") + len("```html")
            end = content.find("```", start)
            content = content[start:end].strip()
        
        return content
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return "There was an error processing your request. Please try again later."

# Function to initialize the file index database (create tables if they don't exist)
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

# Function to initialize the versions database (create tables if they don't exist)
def initialize_versions_db():
    conn = sqlite3.connect(VERSIONS_DB)
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

# Function to save a version of a generated webpage
def save_version(page_name, content):
    conn = sqlite3.connect(VERSIONS_DB)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO web_generator_versions (page_name, timestamp, content)
        VALUES (?, ?, ?)
    ''', (page_name, datetime.now().isoformat(), content))
    conn.commit()
    conn.close()

# Function to get all versions of generated webpages
def get_versions():
    conn = sqlite3.connect(VERSIONS_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT id, page_name, timestamp FROM web_generator_versions ORDER BY timestamp DESC')
    versions = cursor.fetchall()
    conn.close()
    return versions

# Function to get the content of a specific version of a generated webpage
def get_version_by_id(version_id):
    conn = sqlite3.connect(VERSIONS_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM web_generator_versions WHERE id = ?', (version_id,))
    version = cursor.fetchone()
    conn.close()
    return version[0] if version else None
