import os
import sqlite3
import PyPDF2
import pandas as pd
import mimetypes
from bs4 import BeautifulSoup
from utils import initialize_db

# xxtrahera text från olika filtyper
def extract_text(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)  # Hitta filens typ
    if mime_type == 'application/pdf':  # Om det är en PDF-fil
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = "".join(page.extract_text() or "" for page in reader.pages)  # Läs text från varje sida
    elif mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:  # Om det är en Excel-fil
        text = pd.read_excel(file_path).to_string()  # Läs innehåll från Excel-fil
    elif mime_type == 'text/plain':  # Om det är en textfil
        with open(file_path, 'r') as file:
            text = file.read()  # Läs text från textfil
    elif mime_type == 'text/html':  # Om det är en HTML-fil
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            text = soup.get_text()  # Extrahera text från HTML-fil
    else:  # Om filtypen inte stöds
        text = f"Unsupported file type: {mime_type}"  # Meddelande om filtypen inte stöds
    return text

# indexera filer (läsa och spara innehållet i datbasen)
def index_files(folder_path, read_content=True):
    initialize_db()  # Initiera databasen (skapa tabeller om de inte finns)
    conn = sqlite3.connect('file_index.db')  # Anslut till databasen
    cursor = conn.cursor()
    
    # Hitta alla filer i mappen
    current_files = {os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files}
    
    # Hämta alla filer som redan finns i databasen
    cursor.execute('SELECT file_path FROM files')
    db_files = {row[0] for row in cursor.fetchall()}
    
    # Lägg till eller uppdatera aktuella filer i basen
    for file_path in current_files:
        content = extract_text(file_path) if read_content else ""  # Läs filens innehåll om read_content är True
        cursor.execute('''
            INSERT OR REPLACE INTO files (file_path, content)
            VALUES (?, ?)
        ''', (file_path, content))  # Spara filens innehåll i databasen
    
    # radera filer som inte längre finns
    for file_path in db_files - current_files:
        cursor.execute('DELETE FROM files WHERE file_path = ?', (file_path,))
    
    conn.commit()  # Spara ändringar i db
    conn.close()  # Stäng anslutningen till db
    
# hämtar alla indexerade filer
def get_indexed_files(read_content=True):
    conn = sqlite3.connect('file_index.db')  # Anslut till dbs
    cursor = conn.cursor()
    if read_content:
        cursor.execute('SELECT file_path, content FROM files')
        rows = cursor.fetchall()
        files = {row[0]: row[1] for row in rows}  # visas filnamn och innehåll
    else:
        cursor.execute('SELECT file_path FROM files')
        rows = cursor.fetchall()
        files = [row[0] for row in rows]  # visar endast filnamn
    conn.close() 
    return files

# hämta innehåll i en specifik fil
def get_file_content(file_path):
    conn = sqlite3.connect('file_index.db')  # Anslut till databasen
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM files WHERE file_path = ?', (file_path,))
    result = cursor.fetchone()
    conn.close()  # 
    return result[0] if result else "Inget hittat här."  # Returnera filens innehåll eller ett meddelande om inget innehåll finns
