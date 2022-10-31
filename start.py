"""
Imports
"""

import os
from flask import render_template, request
from app import create_app
from models import Person


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route('/', methods=['GET', 'POST'])
def index():
    """
        This is the main route
    """
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def process_jotform():
    """
    This is the process JotForm route
    """
    form_data = request.form.to_dict()

    if form_data["rawRequest"]:
        Person().parse_patient_data(form_data)

    return "ok", 200

if __name__ == '__main__':
    app.run()
