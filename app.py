from flask import Flask, render_template, request
from sqlalchemy import text
from db.models import db, Klant, Docent, Taal, Les

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/cursus_toevoegen", methods=["GET", "POST"])
def cursus_toevoegen():
    if request.method == "POST":
        cursusnaam = request.form["cursusnaam"]
        if cursusnaam:
            new_cursus = Taal(taal=cursusnaam)
            db.session.add(new_cursus)
            db.session.commit()
        return f"Cursus toegevoegd: {cursusnaam}!"
    return render_template("cursus_toevoegen.html")

@app.route("/account_aanmaken", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        gebruikersnaam = request.form["gebruikersnaam"]
        email = request.form["email"]
        wachtwoord = request.form["wachtwoord"]
        if gebruikersnaam:
            new_klant = Docent(gebruikersnaam=gebruikersnaam, email=email, wachtwoord=wachtwoord)
            db.session.add(new_klant)
            db.session.commit()
        return f"Hello, {gebruikersnaam}!"
    return render_template("form.html")

@app.route("/taal_toevoegen", methods=["GET", "POST"])
def taal_toevoegen():
    if request.method == "POST":
        taal = request.form["taal"]
        if taal:
            new_taal = Taal(taal=taal)
            db.session.add(new_taal)
            db.session.commit()
        return f"Mooie, {taal}!"
    return render_template("admin_form.html")


@app.route("/about")
def about():
    return "This is the about page!"



if __name__ == '__main__':
    with app.app_context():    
        db.create_all()
    app.run(debug=True)


