import requests
from bs4 import BeautifulSoup

# Catégories à scraper
categories = [
    "startups",
    "apps",
    "artificial-intelligence"
]

# Fonction pour scraper les articles d'une catégorie | ajout d'une limite de 10 articles par catégorie   
def scrape_category(category, limit = 10):
    url = f"https://techcrunch.com/category/{category}/"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select("li.wp-block-post")
# Limiter le nombre d'articles à 10
    articles = articles[:limit]

    results = []
# Pour chaque article, on récupère le titre et l'URL de l'article, puis on les stocke dans un dictionnaire avec la catégorie correspondante.
    for article in articles:
        title_link = article.select_one("a.loop-card__title-link")

        if title_link:
            title = title_link.get_text(strip=True)
        url = title_link.get("href")

        article_classes = article.get("class", [])

        article_id = None

        for class_name in article_classes:
            if class_name.startswith("post-"):
                article_id = int(class_name.replace("post-", ""))
                break

        results.append({
            "id": article_id,
            "title": title,
            "url": url,
            "category": category
        })

    return results



if __name__ == "__main__":
    categories = [
        "startups",
        "apps",
        "artificial-intelligence"
    ]

    all_articles = []
# Scraper les articles pour chaque catégorie et les stocker dans all_articles
    for category in categories:
        articles = scrape_category(category)

        print(f"{category} : {len(articles)} articles")

        all_articles.extend(articles)

    print(f"\nNombre total d'articles : {len(all_articles)}")
# Afficher les 5 premiers articles pour vérification
    for article in all_articles[:5]:
        print(article)