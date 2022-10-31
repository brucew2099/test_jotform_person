"""
Imports
"""

import json
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Local imports...
from helpers import add_entity, get_next_id


Base = declarative_base()
metadata = Base.metadata

database = SQLAlchemy()
migrate = Migrate()


def setup_db(app):
    """
    Setup database
    """
    database.init_app(app)
    database.app = app
    migrate.init_app(app, database)


class Person(Base):
    """
    Person table
    """
    __tablename__ = 'Persons'
    id = Column('Id', Integer, primary_key=True)
    first_name = Column('FirstName', String(100), nullable=False)
    last_name = Column('LastName', String(100), nullable=False)
    age = Column('Age', Integer, nullable=False)
    form_id = Column('FormId', String(100), nullable=True)
    submission_id = Column('SubmissionId', String(100), nullable=True)
    form_title = Column('FormTitle', String(255), nullable=True)

    def __init__(self, patient_id=0, first_name=None, last_name=None, age=0, 
        form_id=0, submission_id=0, form_title=None):
        self.id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.form_id = form_id
        self.submission_id = submission_id
        self.form_title = form_title


    def __repr__(self):
        return f'Patient class = {self.id}, {self.first_name}, \
            {self.last_name}, {self.age}, \
            {self.form_id}, {self.submission_id}, \
            {self.form_title}'

    def parse_patient_data(self, form_data):
        """
        Parse patient data from request
        :param req:
        :return:
        """
        self.form_id = form_data['formID']
        self.form_title = form_data['formTitle']
        self.submission_id = form_data['submissionID']

        if form_data["rawRequest"]:
            req = json.loads(form_data["rawRequest"])
            self.id = get_next_id(database, Person)
            self.first_name = req['q3_name']['first']
            self.last_name = req['q3_name']['last']
            self.age = req['q4_age']

            add_entity(database, Person)
