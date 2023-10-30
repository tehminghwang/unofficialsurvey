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


def process_query(query_string):
    if query_string == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    if query_string == "asteroids":
        return "Unknown"
    elif "name" in query_string:
        return "teamimperial"
    elif "largest" in query_string:
        listNum = []
        for i in query_string.split():
            if i.isdigit():
                listNum.append(int(i))
                print(listNum)
                temp = ''
        return str(max(listNum))
    else:
        return "Query not recognised"


@app.route("/query", methods=["GET"])
def prog_query():
    query_value = request.args.get("q")
    result = process_query(query_value)
    return result
