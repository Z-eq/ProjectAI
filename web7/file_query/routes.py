import os
import sqlite3
from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from utils import query_openai_gpt
from file_indexer import index_files, get_indexed_files
from datetime import datetime
import logging

#definera en namn på blueprinten.
file_query_bp = Blueprint('file_query', __name__)

# Sökväg till filerna 
DEFAULT_FOLDER_PATH = r'C:\Users\Z\Documents\Skol-Material\Lektioner\Filer'

@file_query_bp.route('/file_query', methods=['GET', 'POST'])
def query_files():
    if request.method == 'POST':
        user_query = request.form['query']
        read_files = 'read_files_toggle' in request.form

        # spara tickboxen för sesionen ( även javascript används)
        session['read_files'] = read_files

       # Definiera fraser som indikerar om att läsa eller räkna filer ( kan lägga till flera)

        file_name_phrases = ["list file names", "visa mina filnamn"]
        file_count_phrases = ["how many files", "hur många filer"]

        #  fraserna
        if any(phrase in user_query.lower() for phrase in file_name_phrases):
            folder_path = DEFAULT_FOLDER_PATH
            index_files(folder_path, read_content=False)
            file_index = get_indexed_files(read_content=False)
            file_names = list(file_index)
            return render_template('file_query.html', query=user_query, response=f"Filerna är: {', '.join(file_names)}")

        if any(phrase in user_query.lower() for phrase in file_count_phrases):
            folder_path = DEFAULT_FOLDER_PATH
            index_files(folder_path, read_content=False)
            file_index = get_indexed_files(read_content=False)
            file_count = len(file_index)
            return render_template('file_query.html', query=user_query, response=f"Du har {file_count} filer indexerade.")

        if read_files:
            # indexera filer vid behov
            folder_path = DEFAULT_FOLDER_PATH
            index_files(folder_path)
            file_index = get_indexed_files()

            # generera en prompt för OpenAI baserat på användares fråga
            openai_prompt = f"You have permission to access and read the contents of the following files:\n{file_index}\nAnswer the question: {user_query}"
        else:
            # Generare en svar utan att få till gång till filerna
            openai_prompt = f"Answer the following question: {user_query}"

        # fråga GPT-3.5 Turbo
        try:
            ai_response = query_openai_gpt(openai_prompt)
            
            # Formatera svaret så det blir finar format på utskift
            formatted_response = ai_response.replace('\n', '<br>').replace('1. ', '<ol><li>').replace('2. ', '<li>').replace('3. ', '<li>').replace('4. ', '<li>').replace('5. ', '<li>').replace('6. ', '<li>').replace('7. ', '<li>').replace('8. ', '<li>').replace('9. ', '<li>') + '</li></ol>'
            
            return render_template('file_query.html', query=user_query, response=formatted_response)
        except Exception as e:
            logging.error(f"Error in teh query: {e}")
            return render_template('file_query.html', query=user_query, response="There was some error,please try again.")
    return render_template('file_query.html', read_files_toggle=session.get('read_files', False))
