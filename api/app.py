from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_pet = request.form.get("pet")
    input_age = request.form.get("age")
    return render_template("confirm.html", pet=input_pet, age=input_age)


def assess_query(q):
    if q == "dinosaurs":
        my_string = "Dinosaurs ruled the Earth 200 million years ago"
        return my_string
    if q == "asteroids":
        my_string = "Unknown"
        return my_string


@app.route("/query")
def process_query():
    query = request.args.get("q")
    result = assess_query(query)
    return result
