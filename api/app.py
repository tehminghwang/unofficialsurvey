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


@app.route("/query", methods=["GET"])
def process_query():
    query_string = request.args.get("q")
    if query_string == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    if query_string == "asteroids":
        return "Unknown"


if __name__ == "__main__":
    app.run(debug=True)
