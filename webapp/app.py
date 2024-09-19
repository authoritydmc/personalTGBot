from flask import Flask, render_template, jsonify, send_from_directory
import os
import logging
from utils import db_util


logger = logging.getLogger(__name__)

app = Flask(__name__)

# Directory where saved media files are stored
MEDIA_DIR = 'data'

@app.route('/')
def index():
    """Render the main page showing the bot status and saved images."""
    # Get the status of the bot (dummy status for this example)
    bot_status = "Running"  # This should be updated dynamically based on actual bot status
    
    # Get the list of saved images
    images = [f for f in os.listdir(MEDIA_DIR) if f.endswith('.jpg')]
    
    return render_template('index.html', bot_status=bot_status, images=images)

@app.route('/status')
def status():
    """Return the status of the bot as JSON."""
    bot_status = "Running"  # This should be updated dynamically based on actual bot status
    return jsonify({'status': bot_status})

@app.route('/images/<filename>')
def get_image(filename):
    """Serve an image from the media directory."""
    return send_from_directory(MEDIA_DIR, filename)

@app.route('/modules')
def modules():
    """Return the list of modules."""
    modules_folder = 'modules'
    modules = [f for f in os.listdir(modules_folder) if f.endswith('.py')]
    return jsonify({'modules': modules})

if __name__ == '__main__':
    # Initialize the database and check tables
    db_util.initialize_db()
    db_util.log_all_tables()
    
    # Run the Flask app
    app.run(debug=True, port=5000)
