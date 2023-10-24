import requests
from bs4 import BeautifulSoup

url = 'https://unofficialsurvey-nine.vercel.app'

reqs = requests.get(url)

soup = BeautifulSoup(reqs.text, 'html.parser')


def test_knows_about_dinosaurs():
    for title in soup.find_all('title'):
        assert title.getText() == 'Unofficial Imperial Survey'
