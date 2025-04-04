from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import text
from website.models import db, Klant, Docent, Cursus, Les, Locatie, User
from flask_login import login_user, login_required, logout_user, current_user
import os
from . import db
import json

views = Blueprint("views", __name__)

@views.route("/", methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html", user=current_user)

@views.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('account/login.html', user=current_user)


@views.route('/register', methods=['GET', 'POST'])
def register():

    # Als het formulier niet is ingediend of niet geldig is, render dan het formulier opnieuw
    return render_template('account/register.html', user=current_user)


@views.route("/cursus_overzicht", methods=["GET"])
@login_required
def cursus_overzicht():
    # if request.method 
    cursussen = db.session.query(Cursus.cursus).all()  # Haal alleen de "name" kolom op
    cursussen = [name[0] for name in cursussen]  # Omdat query.all() een lijst van tuples retourneert
    return render_template("account/cursus_overzicht.html", cursussen=cursussen)

@views.route("/les_maken", methods=["GET", "POST"])
@login_required
def les_maken():
    tijdstippen = [f"{h:02d}:00" for h in range(8, 18)]  # Lijst met tijden van 08:00 tot 17:00

    geselecteerde_tijd = None
    
    geselecteerde_tijd = request.form.get("tijdstip")  # Haal de gekozen tijd op

    # if request.method 
    cursussen = db.session.query(Cursus.cursus).all() 
    cursussen = [name[0] for name in cursussen]  # Omdat query.all() een lijst van tuples retourneert
    # docenten = db.session.query(Docent.id, Docent.gebruikersnaam).all()
    docent_ids = db.session.query(Docent.id).all()
    docent_ids = [id[0] for id in docent_ids]
    docent_namen = db.session.query(Docent.gebruikersnaam).all()
    docent_namen = [naam[0] for naam in docent_namen]
    locaties = db.session.query(Locatie.locatie).all()
    locaties = [locatie[0] for locatie in locaties]
    klant_ids = db.session.query(Klant.id).all()
    klant_ids = [id[0] for id in klant_ids]
    klant_namen = db.session.query(Klant.gebruikersnaam).all()
    klant_namen = [naam[0] for naam in klant_namen]

    if request.method == "POST":
        les_properties = ["klant", "docent_naam", "cursus", "tijdstip", "locatie"]
        les = [request.form[x] for x in les_properties]
        print(les)
        if les:
            new_les = Les(id_klant=les[0], id_docent=les[1], id_cursus=les[2], start_tijd=les[3], locatie=les[4])#list comp
            db.session.add(new_les)
            db.session.commit()

    # print(docent_namen)
    return render_template("admin/les_maken.html", cursussen=cursussen, docent_ids=docent_ids, 
                           docent_namen=docent_namen, locaties=locaties, klant_ids=klant_ids, 
                           klant_namen=klant_namen, tijdstippen=tijdstippen, 
                           geselecteerde_tijd=geselecteerde_tijd)
    
@views.route("/cursus_toevoegen", methods=["GET", "POST"])
@login_required
def cursus_toevoegen():
    if request.method == "POST":
        cursusnaam = request.form["cursusnaam"]
        if cursusnaam:
            new_cursus = Cursus(cursus=cursusnaam)
            db.session.add(new_cursus)
            db.session.commit()
        return f"Cursus toegevoegd: {cursusnaam}!"
    return render_template("admin/cursus_toevoegen.html")


@views.route("/locaties", methods=["GET", "POST"])
@login_required
def locaties():
    if request.method == "POST":
        locatie = request.form["locatie"]
        if locatie:
            new_locatie = Locatie(locatie=locatie)
            db.session.add(new_locatie)
            db.session.commit()
        return f"Locatie toegevoegd: {locatie}!"
    return render_template("admin/locaties.html")

@views.route("/account_aanmaken", methods=["GET", "POST"])
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
    return render_template("account/form.html")


@views.route("/about")
def about():
    return "This is the about page!"



