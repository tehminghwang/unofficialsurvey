from flask import Flask, render_template, request
import re

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/form")
def hello_form():
    return render_template("form.html")

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
        return "teamDOCSSE"
    elif "largest" in query_string:
        numlist = re.findall(r'\d+', query_string)
        return str(max(list(map(int, numlist))))
    elif "plus" in query_string:
        numlist = re.findall(r'\d+', query_string)
        return str(sum(list(map(int, numlist))))
    elif "multiplied" in query_string:
        numlist = re.findall(r'\d+', query_string)
        return str(multiplyList(list(map(int, numlist))))
    elif "prime" in query_string:
        prime_list = []
        numlist = re.findall(r'\d+', query_string)
        for i in numlist:
            x = is_prime(int(i))
            if x == 1:
                prime_list.append(int(i))
        if len(prime_list) == 1:
            return str(prime_list[0])
        else:
            return str(prime_list)
    elif "minus" in query_string:
        numlist = re.findall(r'\d+', query_string)
        return str(is_minus(list(map(int, numlist))))
    elif "cube" in query_string:
        cube_list = []
        numlist = re.findall(r'\d+', query_string)
        for i in numlist:
            if (is_cube(int(i)) & is_square(int(i))):
                cube_list.append(int(i))
        if len(cube_list) == 1:
            return str(cube_list[0])
        else:
            return str(cube_list)
    else:
        return "Query not recognised"


@app.route("/query", methods=["GET"])
def prog_query():
    query_value = request.args.get("q")
    result = process_query(query_value)
    return result


def multiplyList(myList):
    result = 1
    for x in myList:
        result = result * x
    return result


def is_prime(num):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                return 0
        return 1
    return 0


def is_minus(my_list):
    return (my_list[0]-my_list[1])


def is_cube(num) -> bool:
    return round(num ** (1 / 3)) ** 3 == num


def is_square(num) -> bool:
    return round(num ** (1 / 2)) ** 2 == num


#@app.route("/form", methods=["POST"])
#def github():
#    input_user = request.form.get("user")
#    return render_template("confirm.html", user=input_user)
