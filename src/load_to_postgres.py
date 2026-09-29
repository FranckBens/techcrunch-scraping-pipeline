import os  
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)   

print("Connexion bdd réussie !")

cur = conn.cursor()

article = {
    "id": 3162704,
    "title": "Mark Wahlberg is coming to TechCrunch Disrupt 2026, and he wants to talk about your work, not his",
    "url": "https://techcrunch.com/2026/09/25/mark-wahlberg-is-coming-to-techcrunch-disrupt-2026/",
    "description": "Mark Wahlberg joins Bruce K. Lee at TechCrunch Disrupt 2026 to discuss entrepreneurship, investing, and building startups. Register here to join.",
    "author": "TechCrunch Events",
    "published_at": "2026-09-25T18:48:33+00:00",
    "image_url": "https://techcrunch.com/wp-content/uploads/2026/09/TCD26_Wahlberg-Lee-16x9-Dark.png?resize=1200,675"
}

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

conn.commit()

cur.close()
conn.close()

print("Article inséré avec succès !")