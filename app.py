import os
import logging
from flask import Flask, render_template
from file_query.routes import file_query_bp
from web_generator.web_routes import web_generator_bp
from utils import initialize_db

# Starta flaskserver  app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())

# Register blueprints
app.register_blueprint(file_query_bp)
app.register_blueprint(web_generator_bp)

# Koll om outputfolder finns
OUTPUT_FOLDER_PATH = 'static/output'  # om inte, skapar det en
os.makedirs(OUTPUT_FOLDER_PATH, exist_ok=True)


initialize_db()

# simple loggning med lite extra info.
logging.basicConfig(level=logging.DEBUG)  

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
