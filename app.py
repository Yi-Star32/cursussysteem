from mijnproject import app, db
from mijnproject.models import Cursus, Les, Locatie, User, Inschrijving
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from mijnproject.models import User
from mijnproject.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'docent':
        flash('Toegang geweigerd: alleen docenten hebben toegang.')
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
    cursussen = [name[0] for name in cursussen]  # Converteer naar een lijst van cursusnamen
    return render_template("account/cursus_overzicht.html", cursussen=cursussen,form=form)

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
        flash('Toegang geweigerd: alleen docenten hebben toegang.')
        return redirect(url_for('home'))

    geselecteerde_tijd = None
    
    # if request.method 
    cursus_ids = db.session.query(Cursus.id).all()
    cursus_ids = [id[0] for id in cursus_ids]
    cursus_namen = db.session.query(Cursus.cursus).all() 
    cursus_namen = [name[0] for name in cursus_namen]  # Omdat query.all() een lijst van tuples retourneert
    cursussen = {naam: id for naam, id in zip(cursus_namen, cursus_ids)}
    # docenten = db.session.query(Docent.id, Docent.gebruikersnaam).all()
    docent_ids = db.session.query(User.id).filter_by(role='docent').all()
    docent_ids = [id[0] for id in docent_ids]  # Converteer de lijst van tuples naar een lijst van IDs
    docent_namen = db.session.query(User.username).filter_by(role='docent').all()
    docent_namen = [naam[0] for naam in docent_namen]
    docenten = {naam: id for naam, id in zip(docent_namen, docent_ids)}  # {'Piet': 1, 'Henk': 2}

    locaties = db.session.query(Locatie.locatie).all()
    locaties = [locatie[0] for locatie in locaties]
    klant_ids = db.session.query(User.id).filter_by(role='klant').all()
    klant_ids = [id[0] for id in klant_ids]
    klant_namen = db.session.query(User.username).filter_by(role='klant').all()
    klant_namen = [naam[0] for naam in klant_namen]
    klanten = {naam: id for naam, id in zip(klant_namen, klant_ids)}  # {'Jan': 3, 'Kees': 4}

    if request.method == "POST":
        les_properties = ["klant", "docent_naam", "cursus", "datetime", "locatie"]
        les = [request.form[x] for x in les_properties]
        print(les)
        if les:
            new_les = Les(id_klant=klanten[les[0]], id_docent=docenten[les[1]], id_cursus=cursussen[les[2]], start_tijd=les[3], locatie=les[4])#list comp
            db.session.add(new_les)
            db.session.commit()

            flash(f"Les voor: {les[0]} aangemaakt!")
    # print(docent_namen)
    return render_template("admin/les_maken.html", cursussen=cursussen.keys(), 
                           docent_namen=docenten.keys(), locaties=locaties, 
                           klant_namen=klanten.keys(), 
                           geselecteerde_tijd=geselecteerde_tijd)
    
@app.route("/cursus_toevoegen", methods=["GET", "POST"])
@login_required
def cursus_toevoegen():
    if current_user.role != 'docent':
        flash('Toegang geweigerd: alleen docenten hebben toegang.')
        return redirect(url_for('home'))
    if request.method == "POST":
        cursusnaam = request.form["cursusnaam"]
        if cursusnaam:
            new_cursus = Cursus(cursus=cursusnaam)
            db.session.add(new_cursus)
            db.session.commit()
        flash(f"Cursus toegevoegd: {cursusnaam}!")
        return redirect(url_for('home'))        
    return render_template("admin/cursus_toevoegen.html")


@app.route("/locaties", methods=["GET", "POST"])
@login_required
def locaties():
    if current_user.role != 'docent':
        flash('Toegang geweigerd: alleen docenten hebben toegang.')
        return redirect(url_for('home'))
    if request.method == "POST":
        locatie = request.form["locatie"]
        if locatie:
            new_locatie = Locatie(locatie=locatie)
            db.session.add(new_locatie)
            db.session.commit()
        flash(f"Locatie toegevoegd: {locatie}!")
        return redirect(url_for('home'))
    return render_template("admin/locaties.html")


@app.route("/about")
def about():
    return "This is the about page!"



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
    flash('Je bent nu uitgelogd!')
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
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0] == '/':
                next = url_for('welkom')
        

            return redirect(next)
        else:
            flash("Wrong credentials!")
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
        return redirect(url_for('welkom'))  # Stuur de gebruiker naar een welkomspagina

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
