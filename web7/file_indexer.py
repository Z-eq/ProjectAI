import os
import sqlite3
import PyPDF2
import pandas as pd
from PIL import Image
import pytesseract
import mimetypes
from bs4 import BeautifulSoup
from utils import initialize_db

# Funktion för att extrahera text från olika filtyper
def extract_text(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)  # Hitta filens typ
    if mime_type == 'application/pdf':  # Om det är en PDF-fil
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = "".join(page.extract_text() or "" for page in reader.pages)
    elif mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:  # Om det är en Excel-fil
        text = pd.read_excel(file_path).to_string()
    elif mime_type == 'text/plain':  # Om det är en textfil
        with open(file_path, 'r') as file:
            text = file.read()
    elif mime_type == 'text/html':  # Om det är en HTML-fil
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            text = soup.get_text()
    elif mime_type and mime_type.startswith('image/'):  # Om det är en bildfil
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
    else:  # Om filtypen inte stöds
        text = f"Unsupported file type: {mime_type}"
    return text

# Funktion för att indexera filer (läsa och spara innehållet)
def index_files(folder_path, read_content=True):
    initialize_db()  # Initiera databasen (skapa tabeller om de inte finns)
    conn = sqlite3.connect('file_index.db')
    cursor = conn.cursor()
    
    # Hitta alla filer i mappen
    current_files = {os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files}
    
    # Hämta alla filer som redan finns i databasen
    cursor.execute('SELECT file_path FROM files')
    db_files = {row[0] for row in cursor.fetchall()}
    
    # Lägg till eller uppdatera aktuella filer
    for file_path in current_files:
        content = extract_text(file_path) if read_content else ""  # Läs filens innehåll om read_content är True
        cursor.execute('''
            INSERT OR REPLACE INTO files (file_path, content)
            VALUES (?, ?)
        ''', (file_path, content))
    
    # Ta bort filer som inte längre finns
    for file_path in db_files - current_files:
        cursor.execute('DELETE FROM files WHERE file_path = ?', (file_path,))
    
    conn.commit()
    conn.close()

# Funktion för att hämta alla indexerade filer
def get_indexed_files(read_content=True):
    conn = sqlite3.connect('file_index.db')
    cursor = conn.cursor()
    if read_content:
        cursor.execute('SELECT file_path, content FROM files')
        rows = cursor.fetchall()
        files = {row[0]: row[1] for row in rows}  # Returnera filnamn och innehåll
    else:
        cursor.execute('SELECT file_path FROM files')
        rows = cursor.fetchall()
        files = [row[0] for row in rows]  # Returnera bara filnamn
    conn.close()
    return files

# Funktion för att hämta innehållet i en specifik fil
def get_file_content(file_path):
    conn = sqlite3.connect('file_index.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM files WHERE file_path = ?', (file_path,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "No content found."
