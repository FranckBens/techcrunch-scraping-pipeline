import os
import psycopg2
from dotenv import load_dotenv

from extract_article_details import extract_all_articles

load_dotenv()

# Fonctions pour insérer les données dans la base de données PostgreSQL
def insert_article(cur, article):
    cur.execute("""
        INSERT INTO articles (
            id,
            title,
            url,
            description,
            author,
            published_at,
            image_url
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (
        article["id"],
        article["title"],
        article["url"],
        article["description"],
        article["author"],
        article["published_at"],
        article["image_url"]
    ))

# Fonctions pour insérer les catégories et les relations article-catégorie dans la base de données PostgreSQL
def insert_category(cur, category):
    cur.execute("""
        INSERT INTO categories (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
    """, (category,))

# Fonction pour récupérer l'id d'une catégorie à partir de son nom
def get_category_id(cur, category):
    cur.execute("""
        SELECT id
        FROM categories
        WHERE name = %s;
    """, (category,))

    result = cur.fetchone()

    if result:
        return result[0]

    return None

# Fonction pour insérer la relation article-catégorie dans la base de données PostgreSQL
def insert_article_category(cur, article_id, category_id):
    cur.execute("""
        INSERT INTO article_categories (
            article_id,
            category_id
        )
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
    """, (
        article_id,
        category_id
    ))

# Fonction principale pour exécuter le script
def main():

    articles = extract_all_articles()

    print(f"{len(articles)} articles à insérer.")

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    print("Connexion bdd réussie !")

    cur = conn.cursor()

    for article in articles:

        # Insertion de l'article dans la table articles
        insert_article(cur, article)

        
        insert_category(cur, article["category"])


        category_id = get_category_id(
            cur,
            article["category"]
        )

        # Insertion de la relation article-catégorie dans la table article_categories
        if category_id:
            insert_article_category(
                cur,
                article["id"],
                category_id
            )

    conn.commit()

    cur.close()
    conn.close()

    print("Import PostgreSQL terminé !")


if __name__ == "__main__":
    main()