from flask import Flask, render_template, request

app = Flask(__name__)

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
    app.run(debug=True)


