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

# Be sure if output folders exist
OUTPUT_FOLDER_PATH = 'static/output'  # if not create!
os.makedirs(OUTPUT_FOLDER_PATH, exist_ok=True)

# Initialize the database
initialize_db()

# Set basic logging for debug.
logging.basicConfig(level=logging.DEBUG)  # Log more information for debugging

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
