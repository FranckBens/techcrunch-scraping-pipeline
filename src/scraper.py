import requests
from bs4 import BeautifulSoup

# Catégorie à scraper
category = "artificial-intelligence"  # Remplacez par la catégorie souhaitée

URL = f"https://techcrunch.com/category/{category}/"

# Requête HTTP 
response = requests.get(URL)

# Vérification de la requête
response.raise_for_status()

# Analyse du HTML
soup = BeautifulSoup(response.text, "html.parser")

# Récupération de la liste des articles
articles = soup.select("li.wp-block-post")

# Récupération du titre et de l'URL de chaque article
for article in articles:
    title_link = article.select_one("a.loop-card__title-link")

    if title_link:
        title = title_link.get_text(strip=True)
        url = title_link.get("href")

        print("Titre :", title)
        print("URL :", url)
        print("---")