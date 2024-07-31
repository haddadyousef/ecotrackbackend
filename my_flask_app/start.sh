#!/bin/bash
# Change to the application directory
cd my_flask_app
# Activate the virtual environment
source venv/bin/activate
# Initialize the database
python init_db.py
# Start the Flask application
python carbonbackend.py
