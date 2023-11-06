import requests

response = requests.get(“https://api.github.com/users/{GITHUB_USERNAME}/repos”)

if response.status_code == 200:
	repos = response.json() # data returned is a list of ‘repository’ entities
	for repo in repos:
		print(repo[“full_name”])
