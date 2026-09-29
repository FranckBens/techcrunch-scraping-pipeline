import requests
from bs4 import BeautifulSoup


def get_article_details(url):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    description = None
    author = None
    published_at = None
    image_url = None

    # Description
    description_tag = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if description_tag:
        description = description_tag.get("content")

    # Auteur
    author_tag = soup.find(
        "meta",
        attrs={"name": "author"}
    )

    if author_tag:
        author = author_tag.get("content")

    # Date de publication
    published_tag = soup.find(
        "meta",
        attrs={"property": "article:published_time"}
    )

    if published_tag:
        published_at = published_tag.get("content")

    # Image
    image_tag = soup.find(
        "meta",
        attrs={"property": "og:image"}
    )

    if image_tag:
        image_url = image_tag.get("content")

    return {
        "url": url,
        "description": description,
        "author": author,
        "published_at": published_at,
        "image_url": image_url
    }


if __name__ == "__main__":
    from scraper import scrape_category

    categories = [
        "startups",
        "apps",
        "artificial-intelligence"
    ]

    all_articles = []

    for category in categories:
        articles = scrape_category(category)

        for article in articles:
            details = get_article_details(article["url"])

            article.update(details)

            all_articles.append(article)

    print(f"Nombre total d'articles : {len(all_articles)}")

    for article in all_articles[:5]:
        print(article)