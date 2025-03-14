from flask import Flask, render_template, request
from sqlalchemy import text
from db.models import db, Klant, Docent, Taal, Les

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db.init_app(app)

# @app.route("/")
# def index():
#     return "Database is connected!"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        gebruikersnaam = request.form["gebruikersnaam"]
        email = request.form["email"]
        wachtwoord = request.form["wachtwoord"]
        if gebruikersnaam:
            new_klant = Klant(gebruikersnaam=gebruikersnaam, email=email, wachtwoord=wachtwoord)
            db.session.add(new_klant)
            db.session.commit()
        return f"Hello, {gebruikersnaam}!"
    return render_template("form.html")


@app.route("/about")
def about():
    return "This is the about page!"



if __name__ == '__main__':
    with app.app_context():    
        db.create_all()
    app.run(debug=True)


