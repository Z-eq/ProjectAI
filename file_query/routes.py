import os
import sqlite3
from flask import Blueprint, request, render_template, session
from utils import query_openai_gpt
from file_indexer import index_files, get_indexed_files, get_file_content
from datetime import datetime
import logging

# definera blueprinten
file_query_bp = Blueprint('file_query', __name__)

# standard mapp
DEFAULT_FOLDER_PATH = r'C:\Users\Z\Documents\Skol-Material\Lektioner\Filer'

@file_query_bp.route('/file_query', methods=['GET', 'POST'])
def query_files():
    if request.method == 'POST':
        user_query = request.form['query']
        read_files = 'read_files_toggle' in request.form

        #Spara läsafiler instöllning i sessionen
        session['read_files'] = read_files

        # Anv'nd OpenAi för att avgöra en förfrågan
        intent_prompt = f"Determine the intent of this query: {user_query}. Possible intents include 'list file names', 'count files', 'read file contents', or 'general question'."
        intent_response = query_openai_gpt(intent_prompt).lower()

        folder_path = DEFAULT_FOLDER_PATH

        if 'list file names' in intent_response:
            index_files(folder_path, read_content=False)
            file_index = get_indexed_files(read_content=False)
            file_names = list(file_index)
            return render_template('file_query.html', query=user_query, response=f"The files are: {', '.join(file_names)}")

        elif 'count files' in intent_response:
            index_files(folder_path, read_content=False)
            file_index = get_indexed_files(read_content=False)
            file_count = len(file_index)
            return render_template('file_query.html', query=user_query, response=f"You have {file_count} files indexed.")

        elif 'read file contents' in intent_response:
            index_files(folder_path, read_content=True)
            file_index = get_indexed_files(read_content=True)
            # Extract the file name from the query
            file_name = extract_file_name(user_query)
            file_path = os.path.join(folder_path, file_name)
            file_content = get_file_content(file_path)
            openai_prompt = f"Based on the content of the file {file_name}, answer the question: {user_query}\n\n{file_content}"
        else:
            # Läs endast filerna om bocken är ikryssat för (Read files)
            if read_files:
                index_files(folder_path)
                file_index = get_indexed_files()
                openai_prompt = f"You have permission to access and read the contents of the following files:\n{file_index}\nAnswer the question: {user_query}"
            else:
                openai_prompt = f"Answer the following question: {user_query}"

        # Query OpenAI GPT-3.5 Turbo
        try:
            ai_response = query_openai_gpt(openai_prompt)
            formatted_response = ai_response.replace('\n', '<br>').replace('1. ', '<ol><li>').replace('2. ', '<li>').replace('3. ', '<li>').replace('4. ', '<li>').replace('5. ', '<li>').replace('6. ', '<li>').replace('7. ', '<li>').replace('8. ', '<li>').replace('9. ', '<li>') + '</li></ol>'
            return render_template('file_query.html', query=user_query, response=formatted_response)
        except Exception as e:
            logging.error(f"Error processing query: {e}")
            return render_template('file_query.html', query=user_query, response="There was an error processing your request. Please try again later.")

    return render_template('file_query.html', read_files_toggle=session.get('read_files', False))

def extract_file_name(query):
    # Use OpenAI to extract file name from the query
    extraction_prompt = f"Extract the file name from the following query: {query}"
    file_name = query_openai_gpt(extraction_prompt).strip()
    return file_name
