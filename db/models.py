from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Klant(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eerste kolom: Auto-increment ID
    gebruikersnaam = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(100), nullable=False)  
    wachtwoord = db.Column(db.String(100), nullable=False)  # Vierde kolom

    def __repr__(self):
        return f"<Klant {self.id} - {self.gebruikersnaam}>"