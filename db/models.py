from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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


class Taal(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eerste kolom: Auto-increment ID
    taal = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f"<Taal {self.id} - {self.taal}>"
    

class Les(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_klant = db.Column(db.Integer, nullable=False) 
    id_docent = db.Column(db.Integer, nullable=False) 
    id_taal = db.Column(db.Integer, nullable=False) 
    start_tijd = db.Column(db.String(12), nullable=False)
    locatie = db.Column(db.String(50), nullable=False)  

    def __repr__(self):
        return f"<Les {self.id} - {self.id_taal} - {self.start_tijd}>"