import requests
from bs4 import BeautifulSoup

URL = "https://techcrunch.com/category/startups/"

response = requests.get(URL)

print("Status code :", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print("Titre de la page :", soup.title.text)