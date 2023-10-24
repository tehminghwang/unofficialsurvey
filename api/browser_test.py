import requests
from bs4 import BeautifulSoup

url = 'https://unofficialsurvey-nine.vercel.app'

reqs = requests.get(url)

soup = BeautifulSoup(reqs.text,'html.parser')

for title in soup.find_all('title'):
    assert(title.getText() == 'Unofficial Imperial Survey')
