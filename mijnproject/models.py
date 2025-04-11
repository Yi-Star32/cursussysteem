from mijnproject import db, login_manager, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


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
    __tablename__ = 'Klant'
    pass

class Docent(Gebruiker):
    __tablename__ = 'docent'
    pass

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
    

class Les(db.Model):
    __tablename__ = 'les'
    id = db.Column(db.Integer, primary_key=True)
    id_klant = db.Column(db.Integer, nullable=False) 
    id_docent = db.Column(db.Integer, nullable=False) 
    id_cursus = db.Column(db.Integer, nullable=False) 
    start_tijd = db.Column(db.String(12), nullable=False)
    locatie = db.Column(db.String(50), nullable=False)  

    def __repr__(self):
        return f"<Les {self.id} - {self.cursus} - {self.start_tijd}>"

with app.app_context():
    db.create_all()
