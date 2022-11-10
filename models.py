'''
Imports the
'''
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# declarative base class
Base = declarative_base()
metadata = Base.metadata

# Initialize the database connection
db = SQLAlchemy()

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate()

def setup_db(app):
    '''
    Setup the database
    '''
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    return db

session = db.session

class Person(db.Model):
    '''
    This is the base class for all people
    '''
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    form_id = Column(String(50))
    submission_id = Column(String(50))
    form_title = Column(String(100))

    def __repl__(self):
        return f'''
            Last Name: {self.last_name},
            First Name: {self.first_name},
            Age: {self.age},
            Form ID: {self.form_id},
            Submission ID: {self.submission_id},
            Form Title: {self.form_title}
        '''

    def person_to_db(self):
        session.add(self)
        session.commit()
