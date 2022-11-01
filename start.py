"""
Imports
"""

import json
import os
from os.path import abspath, dirname, join
from dotenv import load_dotenv
import pyodbc
from flask import Flask, render_template, request

app = Flask(__name__)

basedir = abspath(dirname(__file__))
load_dotenv(join(basedir, '.env-local'))

DRIVER = os.environ.get('SQLSERVER.DRIVER')
USER = os.environ.get('SQLSERVER.USER')
PASSWD = os.environ.get('SQLSERVER.PASSWD')
HOST = os.environ.get('SQLSERVER.HOST')
DB = os.environ.get('SQLSERVER.DB')

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
        req = json.loads(form_data["rawRequest"])

        conn = pyodbc.connect(f'Driver={DRIVER}; Server={HOST}; \
            Database={DB}; UID={USER}; PWD={PASSWD}; \
            Encrypt=yes; TrustServerCertificate=no; Connection Timeout=30;')

        cursor = conn.cursor()

        next_id = 1

        try:
            cursor.execute("SELECT IDENT_CURRENT('Persons') + 1")
            next_id = 1 if cursor.fetchone()[0] is None else cursor.fetchone()[0]
        except Exception as exception:
            print(exception)
        finally:
            print('There is no record in the table')
            print(f'next_id: {next_id}')

        cursor.execute("INSERT INTO Persons \
            (Id, FirstName, LastName, Age, FormId, SubmissionId, FormTitle) \
            VALUES (?, ?, ?, ?, ?, ?, ?)", (
                next_id,
                req['q3_name']['first'], \
                req['q3_name']['last'], \
                req['q4_age'], \
                form_data['formID'], \
                form_data['submissionID'],\
                form_data['formTitle']))

        # cursor.execute("INSERT INTO Persons \
        #         (Id, FirstName, LastName, Age, FormId, SubmissionId, FormTitle) \
        #         VALUES (?, ?, ?, ?, ?, ?, ?)", (
        #         next_id, 'firstName', 'lastName', \
        #         666, 'formId', 'submissionId', 'formTitle'))

        conn.commit()

        cursor.execute('SELECT * FROM Persons')
        for i in cursor:
            print(i)

        cursor.close()
        conn.close()

    return "ok", 200

if __name__ == '__main__':
    app.run()
