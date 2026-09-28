# import requests bibliothèque pour permettre à Python de faire une requête HTTP -
import requests
from bs4 import BeautifulSoup

URL = "https://techcrunch.com/category/startups/"
# utilisation de la bibliothèque de requests pour faire une requête sur l'url avec python
response = requests.get(URL)
#déchiffrage de la page html 
soup = BeautifulSoup(response.text, "html.parser")

# récuperation de la liste d'article dans la balise <li> avec BS4
articles = soup.select("li.wp-block-post")

# Récupération du titre et de l'url de chaque article
for article in articles:
    title_link = article.select_one("a.loop-card__title-link")

    if title_link:
        title = title_link.get_text(strip=True)
        url = title_link.get("href")

        print("Titre :", title)
        print("URL :", url)
        print("---")
