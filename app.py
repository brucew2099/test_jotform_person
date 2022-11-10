'''
Imports
'''
from datetime import datetime
import os
import json
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from models import Person, setup_db

app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = setup_db(app)

# Create databases, if databases exists doesn't issue create
# For schema changes, run "flask db migrate"
with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    """
        This is the main route
    """
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    """
    This is the process JotForm route
    """
    form_data = request.form.to_dict()
    if form_data["rawRequest"]:
        req = json.loads(form_data["rawRequest"])

        person = Person()
        person.first_name = req['q3_name']['first']
        person.last_name = req['q3_name']['last']
        person.age = req['q4_age']
        person.form_id = form_data['formID']
        person.submission_id = form_data['submissionID']
        person.form_title = form_data['formTitle']
        person.add_person_to_db()

        print(person)
        
    return render_template('addperson.html', person=person)

if __name__ == '__main__':
    app.run()
