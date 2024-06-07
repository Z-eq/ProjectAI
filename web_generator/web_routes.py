import os
import logging
import shutil
import json
from flask import Blueprint, request, render_template, flash, redirect, url_for
from utils import query_openai_gpt, save_version, get_versions, get_version_by_id
from datetime import datetime

web_generator_bp = Blueprint('web_generator', __name__)

OUTPUT_FOLDER_PATH = 'static/output'

def load_template_prompts():
    with open('template_prompts.json', 'r') as file:
        return json.load(file)

TEMPLATE_PROMPTS = load_template_prompts()

@web_generator_bp.route('/web_generator', methods=['GET', 'POST'])
def generate_page():
    if request.method == 'POST':
        page_name = request.form['page_name']
        page_description = request.form['page_description']
        template_choice = request.form.get('template_choice')

        logging.debug(f"Received page_name: {page_name}, page_description: {page_description}, template_choice: {template_choice}")

        if not page_name:
            flash('Page Name is required.', 'danger')
            return redirect(url_for('web_generator.generate_page'))

        # Create a folder for the new page
        page_folder_path = os.path.join(OUTPUT_FOLDER_PATH, page_name)
        os.makedirs(page_folder_path, exist_ok=True)

        if page_description:
            openai_prompt = f"Create a webpage with Bootstrap styles including an info page and login form based on the following description:\n{page_description}"
            html_content = query_openai_gpt(openai_prompt)
        elif template_choice in TEMPLATE_PROMPTS:
            html_content = query_openai_gpt(TEMPLATE_PROMPTS[template_choice])
        else:
            # Use a predefined prompt if no description or template is provided
            with open('default_template.json', 'r') as file:
                default_prompt = json.load(file)['prompt']
            html_content = query_openai_gpt(default_prompt)

        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{page_name}</title>
            <link rel="stylesheet" href="{page_name}.css">
            <script src="{page_name}.js"></script>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        css_content = """
        /* Add your CSS styles here */
        """
        js_content = """
        // Add your JavaScript code here
        """

        try:
            with open(os.path.join(page_folder_path, f"{page_name}.html"), 'w', encoding='utf-8') as file:
                file.write(html_template)
            with open(os.path.join(page_folder_path, f"{page_name}.css"), 'w', encoding='utf-8') as file:
                file.write(css_content)
            with open(os.path.join(page_folder_path, f"{page_name}.js"), 'w', encoding='utf-8') as file:
                file.write(js_content)

            save_version(page_name, html_template)
            page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
            return render_template('web_generator.html', generate_response=f'Webpage generated and saved to <a href="{page_url}" target="_blank">{page_name}.html</a>', versions=get_versions())
        except Exception as e:
            logging.error(f"Error saving files: {e}")
            return render_template('web_generator.html', generate_response="There was an error saving the generated files.", versions=get_versions())
    return render_template('web_generator.html', versions=get_versions())

@web_generator_bp.route('/update_html', methods=['POST'])
def update_html():
    page_name = request.form['page_name']
    update_description = request.form['update_description']

    file_path = os.path.join(OUTPUT_FOLDER_PATH, page_name, f"{page_name}.html")
    backup_file_path = os.path.join(OUTPUT_FOLDER_PATH, page_name, f"{page_name}_backup.html")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_content = file.read()

        shutil.copy(file_path, backup_file_path)
    except Exception as e:
        logging.error(f"Error reading HTML file: {e}")
        return render_template('web_generator.html', update_response="There was an error reading the HTML file.", versions=get_versions())

    # Make prompt more specific
    openai_prompt = f"Update the following HTML content:\n{existing_content}\nBased on this description:\n{update_description}\nMake sure to only change the relevant CSS for the elements described (e.g., navbar, login form) without affecting other parts of the page."
    updated_content = query_openai_gpt(openai_prompt)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        save_version(page_name, updated_content)
        page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
        return render_template('web_generator.html', update_response=f'HTML file updated successfully. <a href="{page_url}" target="_blank">View updated page</a>', versions=get_versions())
    except Exception as e:
        logging.error(f"Error updating HTML file: {e}")
        shutil.copy(backup_file_path, file_path)
        return render_template('web_generator.html', update_response="There was an error updating the HTML file.", versions=get_versions())

@web_generator_bp.route('/rollback', methods=['POST'])
def rollback():
    version_id = request.form['version_id']
    page_name = request.form['page_name']
    version_response = get_version_by_id(version_id)
    if version_response:
        try:
            file_path = os.path.join(OUTPUT_FOLDER_PATH, page_name, f"{page_name}.html")

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(version_response)

            flash('Rollback successful.', 'success')
            page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
            return render_template('web_generator.html', rollback_response=f'Rollback successful. <a href="{page_url}" target="_blank">View rolled back page</a>', versions=get_versions())
        except Exception as e:
            logging.error(f"Error during rollback: {e}")
            return render_template('web_generator.html', rollback_response="There was an error during rollback.", versions=get_versions())
    else:
        flash('Rollback failed. Version not found.', 'danger')
        return render_template('web_generator.html', rollback_response="Rollback failed. Version not found.", versions=get_versions())
