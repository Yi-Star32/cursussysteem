from flask import Flask, render_template, request
from db.models import db, User

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db.init_app(app)

@app.route("/")
def index():
    return "Database is connected!"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        return f"Hello, {name}!"
    return render_template("form.html")

@app.route("/about")
def about():
    return "This is the about page!"



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


