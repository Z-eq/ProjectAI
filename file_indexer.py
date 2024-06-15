import os  
import sqlite3  # Används för att hantera SQLite-databaser
import PyPDF2  # Används för att läsa PDF-filer
import pandas as pd  # Används för att hantera Excel-filer
import mimetypes  # Används för att identifiera filtyper
from bs4 import BeautifulSoup  # Används för att hantera HTML-filer
from utils import initialize_file_index_db  # Importerar funktionen för att initiera filindexdatabasen

# Extrahera text från olika filtyper
def extract_text(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)  # Hitta filens typ
    if mime_type == 'application/pdf':  # Om det är en PDF-fil
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = "".join(page.extract_text() or "" for page in reader.pages)  # Läs text från varje sida
    elif mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:  # Om det är en Excel-fil
        text = pd.read_excel(file_path).to_string()  # Läs innehåll från Excel-fil
    elif mime_type == 'text/plain':  # Om det är en vanlig textfil
        with open(file_path, 'r') as file:
            text = file.read()  # Läs text från filen
    elif mime_type == 'text/html':  # Om det är en HTML-fil
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            text = soup.get_text()  # Extrahera text från HTML-fil genom beautifulsoap
    else:  # Om filtypen inte stöds
        text = f"Filtyp stöds inte: {mime_type}"  # Meddelande om att filtypen inte stöds
    return text  # Returnera extraherad text

# Indexera filer (läsa och spara innehållet i databasen)
def index_files(folder_path, read_content=True):
    initialize_file_index_db()  # Initiera databasen (skapa tabeller om de inte finns)
    conn = sqlite3.connect('file_index.db')  # Anslut till databasen
    cursor = conn.cursor()
    
    # Hitta alla filer i mappen
    current_files = {os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files}
    
    # Hämta alla filer som redan finns i databasen
    cursor.execute('SELECT file_path FROM files')
    db_files = {row[0] for row in cursor.fetchall()}
    
    # Lägg till eller uppdatera aktuella filer i databasen
    for file_path in current_files:
        content = extract_text(file_path) if read_content else ""  # Läs filens innehåll om read_content är True
        cursor.execute('''
            INSERT OR REPLACE INTO files (file_path, content)
            VALUES (?, ?)
        ''', (file_path, content))  # Spara filens innehåll i databasen
    
    # Radera filer som inte längre finns
    for file_path in db_files - current_files:
        cursor.execute('DELETE FROM files WHERE file_path = ?', (file_path,))
    
    conn.commit()  # Spara ändringar i databasen
    conn.close()  # Stäng anslutningen till databasen
    
# Hämta alla indexerade filer
def get_indexed_files(read_content=True):
    conn = sqlite3.connect('file_index.db')  # Anslut till databasen
    cursor = conn.cursor()
    if read_content:
        cursor.execute('SELECT file_path, content FROM files')
        rows = cursor.fetchall()
        files = {row[0]: row[1] for row in rows}  # Returnera filnamn och innehåll
    else:
        cursor.execute('SELECT file_path FROM files')
        rows = cursor.fetchall()
        files = [row[0] for row in rows]  # Returnera bara filnamn
    conn.close()  # Stäng anslutningen till databasen
    return files  # Returnera filerna

# Hämta innehållet i en fil
def get_file_content(file_path):
    conn = sqlite3.connect('file_index.db')  # Anslut till databasen
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM files WHERE file_path = ?', (file_path,))
    result = cursor.fetchone()
    conn.close()  # Stäng anslutningen till databasen
    return result[0] if result else "Inget hittat här."  # Returnera filens innehåll eller ett meddelande om inget innehåll finns
