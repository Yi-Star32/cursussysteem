from mijnproject import db, login_manager, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


# De user_loader decorator zorgt voor de flask-login voor de huidige gebruiker
# en haalt zijn/haar id op.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    # Maak een tabel aan in de database
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), nullable=False, default='klant')  # Nieuwe kolom voor rol

    def __init__(self, email, username, password, role='klant'):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Cursus(db.Model):
    __tablename__ = 'cursus'
    id = db.Column(db.Integer, primary_key=True)  # Eerste kolom: Auto-increment ID
    cursus = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f"<Cursus {self.id} - {self.cursus}>"

class Locatie(db.Model):
    __tablename__ = 'locatie'
    id = db.Column(db.Integer, primary_key=True)  # Eerste kolom: Auto-increment ID
    locatie = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f"<Locatie {self.id} - {self.locatie}>"

class Inschrijving(db.Model):
    __tablename__ = 'inschrijving'
    klant_id = db.Column(db.Integer, primary_key=True, nullable=False)  # Eerste kolom: Auto-increment ID
    cursus_id = db.Column(db.Integer, primary_key=True, nullable=False)


    def __repr__(self):
        return f"<Inschrijving {self.klant_id} - {self.cursus_id}>"
    
    

class Les(db.Model):
    __tablename__ = 'les'
    id = db.Column(db.Integer, primary_key=True)
    id_klant = db.Column(db.Integer, nullable=False) 
    id_docent = db.Column(db.Integer, nullable=False) 
    id_cursus = db.Column(db.Integer, nullable=False) 
    datetime = db.Column(db.DateTime, nullable=False)
    locatie = db.Column(db.String(50), nullable=False)  

    def __repr__(self):
        return f"<Les {self.id} - {self.cursus} - {self.datetime}>"

with app.app_context():
    db.create_all()
