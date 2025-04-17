from mijnproject import app, db
from mijnproject.models import Cursus, Les, Locatie, User, Inschrijving
from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from mijnproject.models import User
from mijnproject.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'docent':
        flash('Toegang geweigerd: alleen docenten hebben toegang.', 'warning')
        return redirect(url_for('home'))
    return render_template('admin/dashboard.html')


@app.route("/cursus_overzicht", methods=["GET", "POST"])
def cursus_overzicht():
    form = RegistrationForm()
    
    if request.method == "POST":
        # Haal de lijst van aangevinkte cursussen op
        geselecteerde_cursussen = request.form.getlist("cursussen")
        if geselecteerde_cursussen:
            for cursus_naam in geselecteerde_cursussen:
                # Zoek de cursus op in de database
                cursus = db.session.query(Cursus).filter_by(cursus=cursus_naam).first()
                if cursus:
                    # Maak een nieuwe inschrijving aan
                    nieuwe_inschrijving = Inschrijving(
                        klant_id=current_user.id,
                        cursus_id=cursus.id
                    )
                    db.session.add(nieuwe_inschrijving)
                    db.session.commit()
            flash(f"Je bent succesvol ingeschreven voor de cursussen: {', '.join(geselecteerde_cursussen)}", "success")
        else:
            flash("Je hebt geen cursus geselecteerd.", "warning")
        return redirect(url_for("cursus_overzicht"))

    # Haal alle cursussen op voor weergave
    cursussen = db.session.query(Cursus.cursus).all()
    kortingen = db.session.query(Cursus.korting).all()
    cursussen = [name[0] for name in cursussen]  # Converteer naar een lijst van cursusnamen
    kortingen = [name[0] for name in kortingen]
    return render_template("account/cursus_overzicht.html", cursussen=cursussen,form=form, kortingen=kortingen)


@app.route('/rooster')
def rooster():
    return render_template('account/rooster.html')


@app.route('/api/lessen', methods=["GET", "POST"])
def get_lessen():
    try:
        if current_user.role == 'docent':
            # Haal lessen op waar de huidige gebruiker de docent is
            lessen = Les.query.filter_by(id_docent=current_user.id).all()
        elif current_user.role == 'klant':
            # Haal lessen op waar de huidige gebruiker de klant is
            lessen = Les.query.filter_by(id_klant=current_user.id).all()
        else:
            flash('Onbekende rol. Kan geen lessen ophalen.', 'danger')
            # return redirect(url_for('home'))
        events = []

        for les in lessen:        
            docent = User.query.get(les.id_docent)
            cursus = Cursus.query.get(les.id_cursus)
            # Voeg toe aan events-lijst in FullCalendar-formaat
            events.append({
                'id': les.id,
                'title': f"{cursus.cursus} - {docent.username}",
                'start': les.datetime.isoformat(),
                'end': (les.datetime.replace(hour=les.datetime.hour+1)).isoformat(),
                'extendedProps': {
                    'locatie': les.locatie,
                    'docent_id': les.id_docent,
                    'cursus_id': les.id_cursus
                }
            })
            return jsonify(events)
    except TypeError as e:
        # Log de fout
        print(f"TypeError bij ophalen lessen: {e}")
        # Retourneer een lege lijst of dummy data
        lessen = []

    # return render_template("account/rooster.html")

@app.route('/process_datetime', methods=['POST'])
def process_datetime():
    datetime_value = request.form.get('datetime')
    # Verwerk de datum en tijd data
    # bijv. opslaan in database, etc.
    
    # Voor debug: print de waarde
    print(f"Ontvangen datum/tijd: {datetime_value}")
    
    # Terug naar homepage of redirect naar een bevestigingspagina
    return redirect(url_for('index'))


@app.route("/les_maken", methods=["GET", "POST"])
@login_required
def les_maken():
    if current_user.role != 'docent':
        flash('Toegang geweigerd: alleen docenten hebben toegang.', 'warning')
        return redirect(url_for('home'))

    geselecteerde_tijd = None
    
    cursus_ids = db.session.query(Cursus.id).all()
    cursus_ids = [id[0] for id in cursus_ids]
    cursus_namen = db.session.query(Cursus.cursus).all() 
    cursus_namen = [name[0] for name in cursus_namen]
    cursussen = {naam: id for naam, id in zip(cursus_namen, cursus_ids)}
    
    docent_ids = db.session.query(User.id).filter_by(role='docent').all()
    docent_ids = [id[0] for id in docent_ids]
    docent_namen = db.session.query(User.username).filter_by(role='docent').all()
    docent_namen = [naam[0] for naam in docent_namen]
    docenten = {naam: id for naam, id in zip(docent_namen, docent_ids)}

    locaties = db.session.query(Locatie.locatie).all()
    locaties = [locatie[0] for locatie in locaties]
    klant_ids = db.session.query(User.id).filter_by(role='klant').all()
    klant_ids = [id[0] for id in klant_ids]
    klant_namen = db.session.query(User.username).filter_by(role='klant').all()
    klant_namen = [naam[0] for naam in klant_namen]
    klanten = {naam: id for naam, id in zip(klant_namen, klant_ids)}

    if request.method == "POST":
        try:
            # Controleer of klanten een lijst is (getlist voor meerdere selecties)
            klant_selectie = request.form.getlist('klanten')
            if not klant_selectie:  # Als getlist niet werkt, probeer een enkele waarde
                klant_selectie = [request.form['klanten']]
                
            # Debug output
            print(f"Geselecteerde klanten: {klant_selectie}")
            
            docent_naam = request.form['docent_naam']
            cursus = request.form['cursus']
            datum_tijd = request.form['datetime']
            locatie = request.form['locatie']
            
            # Converteer de datum-tijd string naar een datetime object
            datum_tijd_obj = datetime.strptime(datum_tijd, '%Y-%m-%d %H:%M')
            
            # Voeg les toe voor elke geselecteerde klant
            for klant_naam in klant_selectie:
                # Controleer of klant bestaat
                if klant_naam in klanten:
                    klant_id = klanten[klant_naam]
                    new_les = Les(
                        id_klant=klant_id, 
                        id_docent=docenten[docent_naam], 
                        id_cursus=cursussen[cursus], 
                        datetime=datum_tijd_obj, 
                        locatie=locatie
                    )
                    db.session.add(new_les)
                else:
                    flash(f"Waarschuwing: Klant '{klant_naam}' niet gevonden", 'warning')
            
            db.session.commit()
            flash(f"Les voor: {', '.join(klant_selectie)} aangemaakt!", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Fout bij het aanmaken van de les: {str(e)}", 'danger')
            print(f"Fout: {str(e)}")
    
    return render_template("admin/les_maken.html", 
                          cursussen=cursussen.keys(), 
                          docent_namen=docenten.keys(), 
                          locaties=locaties, 
                          klant_namen=klanten.keys(), 
                          geselecteerde_tijd=geselecteerde_tijd)
    
@app.route("/cursus_toevoegen", methods=["GET", "POST"])
@login_required
def cursus_toevoegen():
    kortingen = ["Geen Korting", "5%", "10%", "15%", "20%", "50%", "100%"]
    if current_user.role != 'docent':
        flash('Toegang geweigerd: alleen docenten hebben toegang.', 'warning')
        return redirect(url_for('home'))
    if request.method == "POST":
        cursusnaam = request.form["cursusnaam"]
        korting=request.form["korting"]
        if cursusnaam:
            new_cursus = Cursus(cursus=cursusnaam, korting=korting)
            db.session.add(new_cursus)
            db.session.commit()
        flash(f"Cursus toegevoegd: {cursusnaam}!", 'success')
        return redirect(url_for('home'))        
    return render_template("admin/cursus_toevoegen.html",
                           kortingen=kortingen)


@app.route("/locaties", methods=["GET", "POST"])
@login_required
def locaties():
    if current_user.role != 'docent':
        flash('Toegang geweigerd: alleen docenten hebben toegang.', 'warning')
        return redirect(url_for('home'))
    if request.method == "POST":
        locatie = request.form["locatie"]
        if locatie:
            new_locatie = Locatie(locatie=locatie)
            db.session.add(new_locatie)
            db.session.commit()
        flash(f"Locatie toegevoegd: {locatie}!", 'success')
        return redirect(url_for('home'))
    return render_template("admin/locaties.html")




@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welkom')
@login_required
def welkom():
    return render_template('welkom.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!', 'success')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user is not None and user.check_password(form.password.data):
            # Log in the user

            login_user(user)
            flash('Inloggen is gelukt!', 'success')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0] == '/':
                next = url_for('home')
        

            return redirect(next)
        else:
            flash("Foute gegevens!", 'warning')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        is_docent = request.form.get('is_docent') == 'true'  # Controleer of de checkbox is aangevinkt
        role = 'docent' if is_docent else 'klant'  # Stel de rol in op basis van de keuze

        # Maak een nieuwe gebruiker aan
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role=role)

        db.session.add(user)
        db.session.commit()

        # Log de gebruiker direct in
        login_user(user)
        flash('Registratie succesvol! Je bent nu ingelogd.', 'success')
        return redirect(url_for('home'))  # Stuur de gebruiker naar een home

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
