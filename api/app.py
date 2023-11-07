from flask import Flask, render_template, request
import re
import requests
from datetime import datetime
import sys
from io import StringIO

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/code", methods=['GET', 'POST'])
def hello_code():
    code = ''
    result = ''

    if request.method == 'POST':
        code = request.form['code']  # Get code from the form
        result = execute_python_code(code)
        # Process the code here
        return render_template('code.html', code=code, result=result)
    return render_template('code.html')


def execute_python_code(code):
    try:
        # Create a StringIO object to capture the output
        output_buffer = StringIO()
        sys.stdout = output_buffer

        # Execute the Python code
        exec(code)

        # Get the captured output as a string
        captured_output = output_buffer.getvalue()

        result = captured_output

    except Exception as e:
        result = f"Error: {str(e)}"
    finally:
        # Restore the original sys.stdout
        sys.stdout = sys.__stdout__

    return result


@app.route("/form")
def hello_form():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_pet = request.form.get("pet")
    input_age = request.form.get("age")
    return render_template("confirm.html", pet=input_pet, age=input_age)


@app.route("/hello", methods=["POST"])
def github():
    input_user = request.form.get("user")
    response = requests.get(f"https://api.github.com/users/{input_user}/repos")
    if response.status_code == 200:
        repos = response.json()

        # Create an HTML table to display the repository information
        repo_table_html = "<table border='1'><tr><th>Repository Name</th>"
        repo_table_html += "<th>Last Commit Date</th>"
        repo_table_html += "<th>Forks Count</th>"
        repo_table_html += "<th>URL</th>"
        repo_table_html += "<th>Size</th>"
        repo_table_html += "</tr>"

        for repo in repos:
            repo_name = repo['full_name']
            repo_last_commit = repo['pushed_at']
            repo_forks_count = repo['forks_count']
            repo_url = repo['html_url']
            repo_size = repo['size']

        author_tables = []  # List to store author tables
        commit_comment_tables = []  # List to store commit comment tables
        commit_counts = {}  # Dictionary to store commit counts per week
        commit_count_table_html = "<table border='1'><tr><th>Week</th><th>Commit Count</th></tr>"

        for repo in repos:
            repo_name = repo['full_name']
            repo_last_commit = repo['pushed_at']
            repo_forks_count = repo['forks_count']
            repo_url = repo['html_url']
            repo_size = repo['size']

            repo_table_html += f"<tr><td>{repo_name}</td><td>{repo_last_commit}</td><td>{repo_forks_count}</td><td><a href='{repo_url}'>Link</a></td><td>{repo_size}</td></tr>"

            # Fetch and display the commit history for each repository
            commit_history = fetch_commit_history(repo_name)
            commit_table_html = "<table border='1'><tr><th>Commit Message</th><th>Author</th><th>Timestamp</th><th>SHA</th></tr>"
            for commit in commit_history:
                commit_message = commit['commit']['message']
                author_name = commit['commit']['author']['name']
                commit_timestamp = commit['commit']['author']['date']
                commit_sha = commit['sha']
                commit_table_html += f"<tr><td>{commit_message}</td><td>{author_name}</td><td>{commit_timestamp}</td><td>{commit_sha}</td></tr>"
            commit_table_html += "</table>"

            # Fetch and display the list of files for the latest commit
            latest_commit_files = fetch_latest_commit_files(repo_name)
            file_list_html = "<ul>"
            for file in latest_commit_files:
                file_name = file['filename']
                file_download_url = file['raw_url']
                file_list_html += f"<li><a href='{file_download_url}'>{file_name}</a></li>"
            file_list_html += "</ul>"

            repo_table_html += f"<tr><td colspan='5'>{commit_table_html}<br>{file_list_html}</td></tr>"

            # Fetch and display the commit history for each repository
            commit_history = fetch_commit_history(repo_name)
            commit_table_html = "<table border='1'><tr><th>Commit Message</th><th>Author</th><th>Timestamp</th><th>SHA</th></tr>"
            commit_comments = set()
            authors = set()
            for commit in commit_history:
                commit_message = commit['commit']['message']
                author_name = commit['commit']['author']['name']
                commit_timestamp = commit['commit']['author']['date']
                commit_sha = commit['sha']
                commit_table_html += f"<tr><td>{commit_message}</td><td>{author_name}</td><td>{commit_timestamp}</td><td>{commit_sha}</td></tr>"
                commit_comments.add(commit_message)
                authors.add(author_name)
                commit_date = commit_timestamp.split('T')[0]
                commit_week = f"Week {datetime.strptime(commit_date, '%Y-%m-%d').strftime('%U, %Y')}"
                commit_counts[commit_week] = commit_counts.get(commit_week, 0) + 1
            commit_table_html += "</table>"

            # Append the commit table to the repository table
            repo_table_html += f"<tr><td colspan='5'>{commit_table_html}</td></tr>"

            # Create an author table
            author_table_html = "<table border='1'><tr><th>Unique Authors</th></tr>"
            for author in authors:
                author_table_html += f"<tr><td>{author}</td></tr>"
            author_table_html += "</table>"
            author_tables.append(author_table_html)

            # Create a commit comment table
            commit_comment_table_html = "<table border='1'><tr><th>Unique Commit Comments</th><th>Count</th></tr>"
            for comment in commit_comments:
                count = sum(1 for commit in commit_history if commit['commit']['message'] == comment)
                commit_comment_table_html += f"<tr><td>{comment}</td><td>{count}</td></tr>"
            commit_comment_table_html += "</table>"
            commit_comment_tables.append(commit_comment_table_html)

        repo_table_html += "</table>"

        return repo_table_html
    else:
        return 'No response'

        # Append the author tables and commit comment tables to the repository table
        for author_table, commit_comment_table in zip(author_tables, commit_comment_tables):
            repo_table_html += f"{author_table}{commit_comment_table}"

        # Filter and combine commit count per week table
        commit_count_table_html += "<table border='1'>"
        for week, count in commit_counts.items():
            if 'Week 40' <= week <= 'Week 45':
                commit_count_table_html += f"<tr><td>{week}</td><td>{count}</td></tr>"
                commit_count_table_html += "</table>"

                return repo_table_html + commit_count_table_html
            else:
                return 'No response'


def fetch_commit_history(repo_name):
    response = requests.get(f"https://api.github.com/repos/{repo_name}/commits")
    if response.status_code == 200:
        return response.json()
    return []


def fetch_latest_commit_files(repo_name):
    response = requests.get(f"https://api.github.com/repos/{repo_name}/commits/master/files")
    if response.status_code == 200:
        return response.json()
    return []


if __name__ == "__main__":
    app.run(debug=True)


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
    return (my_list[0] - my_list[1])


def is_cube(num) -> bool:
    return round(num ** (1 / 3)) ** 3 == num


def is_square(num) -> bool:
    return round(num ** (1 / 2)) ** 2 == num
