import os  
import sqlite3  # Används för att hantera SQLite-databaser
from flask import Blueprint, request, render_template, session 
""" Importerar Blueprint för att dela upp Flask-applikationen i moduler, 
request för att hantera inkommande förfrågningar, render_template för att visa HTML-sidor och session för att lagra användardata mellan förfrågningar """
from utils import query_openai_gpt  # Importerar funktionen för att fråga OpenAI GPT
from file_indexer import index_files, get_indexed_files, get_file_content  # Importerar funktioner för att indexera filer och hämta filinnehåll
from datetime import datetime 
import logging  # Används för att logga meddelanden

# Definiera blueprint för filförfrågningar
file_query_bp = Blueprint('file_query', __name__)

# Standardmapp för filer
DEFAULT_FOLDER_PATH = r'Filer'

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
