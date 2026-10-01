import requests
from bs4 import BeautifulSoup


# Catégories TechCrunch à scraper
CATEGORIES = [
    "startups",
    "apps",
    "artificial-intelligence"
]


def scrape_category(category, limit=10):
    """Scrape les articles d'une catégorie TechCrunch."""

    url = f"https://techcrunch.com/category/{category}/"

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select("li.wp-block-post")[:limit]

    results = []

    for article in articles:
        title_link = article.select_one("a.loop-card__title-link")

        if not title_link:
            continue

        title = title_link.get_text(strip=True)
        url = title_link.get("href")

        article_classes = article.get("class", [])

        article_id = None
        tags = []

        for class_name in article_classes:
            if class_name.startswith("post-"):
                article_id = int(class_name.replace("post-", ""))

            if class_name.startswith("tag-"):
                tags.append(class_name.replace("tag-", ""))

        results.append({
            "id": article_id,
            "title": title,
            "url": url,
            "category": category,
            "tags": tags
        })

    return results


if __name__ == "__main__":
    all_articles = []

    for category in CATEGORIES:
        articles = scrape_category(category)

        print(f"{category} : {len(articles)} articles")

        all_articles.extend(articles)

    print(f"\nNombre total d'articles : {len(all_articles)}")

    for article in all_articles[:5]:
        print(article)