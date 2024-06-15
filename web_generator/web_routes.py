import os  
import logging 
import json  # Används för att tolka JSON-data
from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify  # Importerar Flask-moduler för att hantera webbruttar och rendering
from utils import query_openai_gpt, save_version, get_versions, get_version_by_id  # Importerar hjälpfunktioner för blandannat databas funktioner
from datetime import datetime 

# Skapar en blueprint för webbgeneratorn
web_generator_bp = Blueprint('web_generator', __name__)

# Standardmapp för att spara skapade websidor
OUTPUT_FOLDER_PATH = 'static/output'
os.makedirs(OUTPUT_FOLDER_PATH, exist_ok=True)  # Skapar mappen om den inte finns

# Laddar mallar för prompts från en JSON-fil
def load_template_prompts():
    with open('template_prompts.json', 'r') as file:
        return json.load(file)

# Sparar mallarna i en variabel
TEMPLATE_PROMPTS = load_template_prompts()

# Definierar en rutt för att generera en webbsida
@web_generator_bp.route('/web_generator', methods=['GET', 'POST'])
def generate_page():
    if request.method == 'POST':  # Kolla att förfrågan är en POST
        page_name = request.form['page_name']  # Hämta sidnamnet från namn formen
        page_description = request.form['page_description']  # Hämta sidbeskrivningen från description formuläret
        template_choice = request.form.get('template_choice')  # Hämta vald mall från formuläret

        logging.debug(f"Received page_name: {page_name}, page_description: {page_description}, template_choice: {template_choice}")

        if not page_name:  # Om sidnamnet saknas, visa ett felmeddelande
            flash('Page Name is required.', 'danger')
            return redirect(url_for('web_generator.generate_page'))

        page_folder_path = os.path.join(OUTPUT_FOLDER_PATH, page_name)  # Skapa en mapp för sidan
        os.makedirs(page_folder_path, exist_ok=True)  # Skapa mappen om den inte finns

        if page_description:  # Om sidbeskrivning finns, använd den för att skapa prompten
            openai_prompt = page_description
            html_content = query_openai_gpt(openai_prompt)  # Fråga OpenAI med beskrivningen
        elif template_choice in TEMPLATE_PROMPTS:  # Om en mall är vald, använd den
            html_content = query_openai_gpt(TEMPLATE_PROMPTS[template_choice])
        else:  # Annars, använd en standardmall
            with open('default_template.json', 'r') as file:
                default_prompt = json.load(file)['prompt']
            html_content = query_openai_gpt(default_prompt)

        # Skapar HTML-mallen för sidan
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
        /* Lägg till önsakt fövalt CSS  här */
        """
        js_content = """
        // Lägg till din JavaScript-kod här
        """

        try:
            # Spara HTML-filen i skrivläge
            with open(os.path.join(page_folder_path, f"{page_name}.html"), 'w', encoding='utf-8') as file:
                file.write(html_template)
            # Spara CSS-filen i skrivläge 
            with open(os.path.join(page_folder_path, f"{page_name}.css"), 'w', encoding='utf-8') as file:
                file.write(css_content)
            # Spara JS-filen i skrivläge
            with open(os.path.join(page_folder_path, f"{page_name}.js"), 'w', encoding='utf-8') as file:
                file.write(js_content)

            # Spara en version av sidan
            save_version(page_name, html_template)
            page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
            return render_template('web_generator.html', generate_response=f'Webpage generated and saved to <a href="{page_url}" target="_blank">{page_name}.html</a>', versions=get_versions())
        except Exception as e:  # Hantera eventuella fel
            logging.error(f"Error saving files: {e}")
            return render_template('web_generator.html', generate_response="There was an error saving the generated files.", versions=get_versions())
    return render_template('web_generator.html', versions=get_versions())

# Definierar en route för att uppdatera en HTML-sida
@web_generator_bp.route('/update_html', methods=['POST'])
def update_html():
    page_name = request.form['page_name']  # Hämta sidnamnet från formuläret
    update_description = request.form['update_description']  # Hämta uppdateringsbeskrivningen från formuläret

    file_path = os.path.join(OUTPUT_FOLDER_PATH, page_name, f"{page_name}.html")  # Hämta filvägen

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_content = file.read()  # Läs det befintliga innehållet
    except Exception as e:
        logging.error(f"Error reading HTML file: {e}")
        return render_template('web_generator.html', update_response="There was an error reading the HTML file.", versions=get_versions())

    # Lägg till specifika instruktioner för att säkerställa att rätt uppdateringar görs när man frågar OpenAI ( man kan ändra promten till mer specifkt)
    openai_prompt = f"Here is the current HTML content:\n\n{existing_content}\n\nUpdate it based on the following description:\n\n{update_description}\n\nMake sure to only change the relevant sections and keep the rest of the content intact."
    updated_content = query_openai_gpt(openai_prompt)  # Fråga OpenAI med den uppdaterade beskrivningen

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)  # Skriv det uppdaterade innehållet

        save_version(page_name, updated_content)  # Spara en version av uppdateringen i versions.db basen
        page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
        return render_template('web_generator.html', update_response=f'HTML file updated successfully. <a href="{page_url}" target="_blank">View updated page</a>', versions=get_versions())
    except Exception as e:
        logging.error(f"Error updating HTML file: {e}")
        return render_template('web_generator.html', update_response="There was an error updating the HTML file.", versions=get_versions())

# Definierar en rutt för att återgå till en tidigare version
@web_generator_bp.route('/rollback', methods=['POST'])
def rollback():
    version_id = request.form['version_id']  # Hämta versions-ID från formuläret
    page_name = request.form['page_name']  # Hämta sidnamnet från formuläret
    
    logging.debug(f"Rollback requested for version_id: {version_id}, page_name: {page_name}")
    
    version_response = get_version_by_id(version_id)  # Hämta innehållet för den specifika versionen
    if version_response:
        try:
            file_path = os.path.join(OUTPUT_FOLDER_PATH, page_name, f"{page_name}.html")  # Hämta filvägen
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(version_response)  # Skriv versionens innehåll till filen
            
            flash('Rollback successful.', 'success')  # Visa ett meddelande om att återställningen lyckades
            page_url = url_for('static', filename=f'output/{page_name}/{page_name}.html')
            return render_template('web_generator.html', rollback_response=f'Rollback successful. <a href="{page_url}" target="_blank">View rolled back page</a>', versions=get_versions())
        except Exception as e:
            logging.error(f"Error during rollback: {e}")
            return render_template('web_generator.html', rollback_response="There was an error during rollback.", versions=get_versions())
    else:
        flash('Rollback failed. Version not found.', 'danger')  # Visa ett felmeddelande om versionen inte hittades
        return render_template('web_generator.html', rollback_response="Rollback failed. Version not found.", versions=get_versions())
