# TechCrunch Scraping Pipeline

A Python data pipeline that extracts articles from multiple TechCrunch categories, enriches the collected data, and stores it in a structured PostgreSQL database.

## 🎯 Project Overview

The goal of this project is to build a simple ETL pipeline:

1. **Extract** — Scrape articles from TechCrunch category pages.
2. **Transform** — Extract and structure additional metadata from each article.
3. **Load** — Store the collected data in PostgreSQL.

The pipeline currently retrieves up to 10 articles from each of the following categories:

- `startups`
- `apps`
- `artificial-intelligence`

---

## 🏗️ Pipeline Architecture

```text
TechCrunch
    │
    ▼
Category pages
    │
    ▼
scraper.py
    │
    │  Article ID
    │  Title
    │  URL
    │  Category
    │  Tags
    ▼
extract_article_details.py
    │
    │  Description
    │  Author
    │  Publication date
    │  Image URL
    ▼
load_to_postgres.py
    │
    ▼
PostgreSQL
    │
    ├── articles
    ├── categories
    ├── tags
    ├── article_categories
    └── article_tags
```

The scraping process is split into two stages. The category pages provide the initial article information, while each article page is then requested individually to retrieve additional metadata.

---

## 🔎 Collected Data

For each article, the pipeline collects:

- Article ID
- Title
- URL
- Description
- Author
- Publication date
- Image URL
- Category
- Tags

Some metadata may be unavailable depending on the type of TechCrunch content. In this case, nullable fields are stored as `NULL` in PostgreSQL.

---

## 🗄️ Data Model

The PostgreSQL database is composed of five tables:

- `articles` — stores the main article information
- `categories` — stores unique categories
- `tags` — stores unique article tags
- `article_categories` — association table between articles and categories
- `article_tags` — association table between articles and tags

The database uses a normalized relational model:

```text
                    ┌──────────────┐
                    │  categories  │
                    └──────┬───────┘
                           │
                           │
                ┌──────────▼───────────┐
                │ article_categories   │
                └──────────┬───────────┘
                           │
                           │
                    ┌──────▼───────┐
                    │   articles   │
                    └──────┬───────┘
                           │
                           │
                  ┌────────▼────────┐
                  │  article_tags   │
                  └────────┬────────┘
                           │
                           │
                     ┌─────▼─────┐
                     │   tags    │
                     └───────────┘
```

This structure supports many-to-many relationships and makes it possible to add new categories and tags without changing the database schema.

---

## 🛠️ Tech Stack

- **Python** — Core pipeline logic
- **Requests** — HTTP requests
- **BeautifulSoup** — HTML parsing and web scraping
- **PostgreSQL** — Relational data storage
- **psycopg2** — PostgreSQL connection from Python
- **python-dotenv** — Environment variable management

---

## 📂 Project Structure

```text
techcrunch-scraping-pipeline/
│
├── src/
│   ├── scraper.py
│   ├── extract_article_details.py
│   └── load_to_postgres.py
│
├── sql/
│   └── create_table.sql
│
├── data/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Main files

- `scraper.py` — extracts article IDs, titles, URLs, categories, and tags from TechCrunch category pages.
- `extract_article_details.py` — enriches each article with its description, author, publication date, and image URL.
- `load_to_postgres.py` — loads articles and their relationships into PostgreSQL.
- `create_table.sql` — creates the PostgreSQL database schema.

---

## 🚀 Getting Started

### Prerequisites

Make sure the following tools are installed:

- Python 3
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/FranckBens/techcrunch-scraping-pipeline.git
cd techcrunch-scraping-pipeline
```

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv venv
```

Activate the virtual environment with PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell prevents script execution, it can also be activated from Command Prompt:

```cmd
venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

#### Windows

```powershell
pip install -r requirements.txt
```

#### macOS / Linux

```bash
pip3 install -r requirements.txt
```

### 4. Configure the environment variables

Create a `.env` file at the root of the project based on `.env.example`:

```env
DB_NAME=techcrunch_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

The `.env` file contains local database credentials and must not be committed to Git.

### 5. Create the PostgreSQL database

Create a PostgreSQL database named:

```text
techcrunch_db
```

Then execute the SQL script located at:

```text
sql/create_table.sql
```

The script can be executed using pgAdmin or any PostgreSQL client connected to techcrunch_db.
It creates the five tables required by the pipeline:

- `articles`
- `categories`
- `tags`
- `article_categories`
- `article_tags`

---

## ▶️ Usage

Once PostgreSQL is running and the environment variables are configured, run the complete pipeline.

### Windows

```powershell
python src/load_to_postgres.py
```

### macOS / Linux

```bash
python3 src/load_to_postgres.py
```

The pipeline will:

1. Scrape the configured TechCrunch categories.
2. Retrieve up to 10 articles per category.
3. Enrich each article with additional metadata.
4. Insert the articles into PostgreSQL.
5. Insert categories and tags.
6. Create the corresponding article-category and article-tag relationships.


### Windows

```powershell
python src/scraper.py
python src/extract_article_details.py
```

### macOS / Linux

```bash
python3 src/scraper.py
python3 src/extract_article_details.py
```

---

## 🔍 Database Verification

After running the pipeline, the imported data can be checked with SQL queries such as:

```sql
SELECT COUNT(*) FROM articles;

SELECT * FROM categories;

SELECT * FROM tags;

SELECT COUNT(*) FROM article_categories;

SELECT COUNT(*) FROM article_tags;
```

To inspect articles with their categories:

```sql
SELECT
    a.id,
    a.title,
    c.name AS category
FROM articles a
JOIN article_categories ac
    ON a.id = ac.article_id
JOIN categories c
    ON ac.category_id = c.id;
```

---

## 🧠 Technical Choices

### PostgreSQL

PostgreSQL was chosen because the collected data contains clear relationships between articles, categories, and tags. A relational database makes these relationships easy to model and query.

### Many-to-many relationships

An article may appear across multiple TechCrunch categories and can have multiple tags.

Association tables (`article_categories` and `article_tags`) are therefore used to keep the database normalized and avoid duplicating article data.

### Limited scraping

The scraper currently retrieves up to 10 articles per category.

The purpose of this limit is to demonstrate the complete ETL workflow without unnecessarily scraping the entire website.

### Duplicate management

Database constraints combined with PostgreSQL `ON CONFLICT DO NOTHING` statements prevent duplicate records and duplicate relationships when the pipeline is executed multiple times.

---

## ⚠️ Current Limitations

- The pipeline depends on the current HTML structure of TechCrunch.
- Existing articles are not updated because conflicts are currently ignored with `ON CONFLICT DO NOTHING`.
- HTTP retry mechanisms are not implemented yet.
- Some TechCrunch content types may not provide all article metadata.
- The pipeline is currently executed manually.

---

## 🔮 Possible Improvements

Possible next steps include:

- Dockerize the Python application and PostgreSQL database
- Build a REST API with FastAPI
- Add automated tests with `pytest`
- Add structured logging
- Add HTTP retry and more advanced error handling
- Schedule and orchestrate the pipeline with Apache Airflow
- Add CI/CD with GitHub Actions
- Implement upserts to update existing articles
- Make the list of categories configurable

---

## 📄 License

This project was created for educational and technical assessment purposes.