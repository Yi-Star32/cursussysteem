from mijnproject import app, db
from mijnproject.models import Cursus, Les, Locatie, User
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

@app.route("/cursus_overzicht", methods=["GET"])
def cursus_overzicht():
    # if request.method 
    cursussen = db.session.query(Cursus.cursus).all()  # Haal alleen de "name" kolom op
    cursussen = [name[0] for name in cursussen]  # Omdat query.all() een lijst van tuples retourneert
    return render_template("account/cursus_overzicht.html", cursussen=cursussen)

@app.route("/les_maken", methods=["GET", "POST"])
@login_required
def les_maken():
    if current_user.role != 'docent':
        flash('Toegang geweigerd: alleen docenten hebben toegang.')
        return redirect(url_for('home'))
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
        return f"Cursus toegevoegd: {cursusnaam}!"
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
        return f"Locatie toegevoegd: {locatie}!"
    return render_template("admin/locaties.html")

@app.route("/account_aanmaken", methods=["GET", "POST"])
def account_aanmaken():
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
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        is_docent = request.form.get('is_docent') == 'true'  # Controleer of de checkbox is aangevinkt
        role = 'docent' if is_docent else 'klant'  # Stel de rol in op basis van de keuze

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role=role)

        db.session.add(user)
        db.session.commit()
        flash('Dank voor de registratie. Er kan nu ingelogd worden!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
