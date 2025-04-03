from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

from utils import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm

db = SQLAlchemy()

# class RegistrationForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(),Email()])
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
#     pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
#     submit = SubmitField('Submit!')

# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Inloggen')

class User(db.Model, UserMixin):
    # Maak een tabel aan in de database
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    

class Gebruiker(db.Model):
    __abstract__ = True  # Zorgt ervoor dat deze klasse geen eigen tabel krijgt
    id = db.Column(db.Integer, primary_key=True)  # Eerste kolom: Auto-increment ID
    gebruikersnaam = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(100), nullable=False)  
    wachtwoord = db.Column(db.String(100), nullable=False)  # Vierde kolom

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} - {self.gebruikersnaam}>"

class Klant(Gebruiker):
    pass

class Docent(Gebruiker):
    pass


class Cursus(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eerste kolom: Auto-increment ID
    cursus = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f"<Cursus {self.id} - {self.cursus}>"

class Locatie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eerste kolom: Auto-increment ID
    locatie = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f"<Locatie {self.id} - {self.locatie}>"
    

class Les(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_klant = db.Column(db.Integer, nullable=False) 
    id_docent = db.Column(db.Integer, nullable=False) 
    id_cursus = db.Column(db.Integer, nullable=False) 
    start_tijd = db.Column(db.String(12), nullable=False)
    locatie = db.Column(db.String(50), nullable=False)  

    def __repr__(self):
        return f"<Les {self.id} - {self.cursus} - {self.start_tijd}>"
    
