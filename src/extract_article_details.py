import requests
from bs4 import BeautifulSoup
from scraper import scrape_category

# Fonction pour extraire les détails d'un article à partir de son URL
def get_article_details(url):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=10
    )

    response.raise_for_status()
# Utilisation de BeautifulSoup pour parser le contenu HTML de la page
    soup = BeautifulSoup(response.text, "html.parser")
# Initialisation des variables pour stocker les détails de l'article
    description = None
    author = None
    published_at = None
    image_url = None

# Récupération de la description de l'article
    description_tag = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if description_tag:
        description = description_tag.get("content")

# Récupération de l'auteur de l'article
    author_tag = soup.find(
        "meta",
        attrs={"name": "author"}
    )

    if author_tag:
        author = author_tag.get("content")

# Récupération de la date de publication de l'article
    published_tag = soup.find(
        "meta",
        attrs={"property": "article:published_time"}
    )

    if published_tag:
        published_at = published_tag.get("content")

# Récupération de l'URL de l'image de l'article
    image_tag = soup.find(
        "meta",
        attrs={"property": "og:image"}
    )

    if image_tag:
        image_url = image_tag.get("content")
# Retourne un dictionnaire contenant les détails de l'article
    return {
        "description": description,
        "author": author,
        "published_at": published_at,
        "image_url": image_url
    }

# Fonction pour extraire les détails de tous les articles
if __name__ == "__main__":
    from scraper import scrape_category
def extract_all_articles():
    categories = [
        "startups",
        "apps",
        "artificial-intelligence"
    ]
# Scraper les articles pour chaque catégorie et les stocker dans all_articles
    all_articles = []

    for category in categories:
        articles = scrape_category(category)

        for article in articles:
            details = get_article_details(article["url"])
            article.update(details)
            all_articles.append(article)

    return all_articles

# Test de la fonction extract_all_articles
if __name__ == "__main__":
    all_articles = extract_all_articles()

    print(f"Nombre total d'articles : {len(all_articles)}")

    for article in all_articles[:5]:
        print(article)