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


def process_query(q):
    if q == "dinosaurs":
        my_string = "Dinosaurs ruled the Earth 200 million years ago"
    if q == "asteroids":
        my_string = "Unknown"
    return my_string


@app.route("/query", methods=["GET"])
def query_endpoint():
    query = request.args.get("q")
    result = process_query(query)
    return result


if __name__ == "__main__":
    app.run(debug=True)
