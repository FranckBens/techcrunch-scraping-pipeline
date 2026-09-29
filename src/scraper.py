import requests
from bs4 import BeautifulSoup

# Catégories à scraper
categories = [
    "startups",
    "apps",
    "artificial-intelligence"
]


def scrape_category(category):
    url = f"https://techcrunch.com/category/{category}/"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select("li.wp-block-post")

    results = []

    for article in articles:
        title_link = article.select_one("a.loop-card__title-link")

        if title_link:
            results.append({
                "title": title_link.get_text(strip=True),
                "url": title_link.get("href"),
                "category": category
            })

    return results


# Liste finale de tous les articles
all_articles = []

for category in categories:
    articles = scrape_category(category)

    print(f"{category} : {len(articles)} articles")

    all_articles.extend(articles)


print(f"\nNombre total d'articles : {len(all_articles)}")

# Affichage des 5 premiers articles
for article in all_articles[:5]:
    print(article)