<div align="center">

# 📚 Book Search Engine

**A full-stack search application with real-time autocomplete, typo-tolerant full-text search, and relevance ranking**
</div>

---

## 📌 Overview

Book Search Engine is a production-inspired search application that covers the **complete lifecycle of a search system** — from raw CSV data ingestion and Elasticsearch indexing, to a REST API and a responsive frontend with live search.

Users can search across 10,000+ books by title, author, genre, or description. Results are ranked by relevance, tolerant of typos, and delivered in under 100ms. As users type, autocomplete suggestions appear instantly using prefix-based queries.

This project was built entirely from scratch without any frontend framework or third-party search UI library, demonstrating end-to-end ownership of a full-stack system.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔍 Full-text search | Multi-field search across title, author, genre, and description |
| 🧠 Relevance ranking | BM25 scoring with custom field boosts (title ×10, author ×2) |
| ✏️ Typo tolerance | Elasticsearch `fuzziness: AUTO` handles misspellings automatically |
| ⚡ Real-time autocomplete | `match_phrase_prefix` query with live dropdown as you type |
| 📖 Rich book cards | Cover thumbnail, title, author, genre, description, star rating |
| 🌐 REST API | Clean Flask endpoints consumed by vanilla JavaScript fetch |
| 📦 Data pipeline | CSV ingestion and indexing with pandas |
| 📱 Responsive UI | Mobile-friendly layout with CSS flexbox |
| 🔐 Secure config | Credentials managed via environment variables, never hardcoded |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          BROWSER                                │
│                                                                 │
│   ┌───────────────────────────────────────────────────────┐    │
│   │            index.html  ·  style.css                   │    │
│   │                                                       │    │
│   │   [Search Input] ──onInput──▶ fetchSuggestions()      │    │
│   │                                    │                  │    │
│   │                          GET /autocomplete?q=         │    │
│   │                                    │                  │    │
│   │   [Search Button] ──onClick──▶ search()               │    │
│   │                                    │                  │    │
│   │                            GET /search?q=             │    │
│   └────────────────────────────────────┬──────────────────┘    │
└────────────────────────────────────────│────────────────────────┘
                                         │  HTTP · localhost:5000
┌────────────────────────────────────────▼────────────────────────┐
│                     FLASK REST API  (app.py)                    │
│                                                                 │
│   GET /search        ──▶  bool query  (multi_match + boost)    │
│   GET /autocomplete  ──▶  match_phrase_prefix                  │
│   GET /count         ──▶  document count                       │
└────────────────────────────────────────┬────────────────────────┘
                                         │  Elasticsearch Python Client
┌────────────────────────────────────────▼────────────────────────┐
│              ELASTICSEARCH 8.x  (localhost:9200)                │
│                                                                 │
│   Index: search_engine                                          │
│   Fields: title · author · genre · description                  │
│           publisher · language · rating · thumbnail             │
└────────────────────────────────────────┬────────────────────────┘
                                         ▲
                              pandas + es.index()
┌────────────────────────────────────────┴────────────────────────┐
│               DATA PIPELINE  (load_books.py)                    │
│                                                                 │
│   Books.csv  ──pandas──▶  row dicts  ──index──▶  Elasticsearch │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 How Search & Ranking Works

Search uses Elasticsearch's **BM25 algorithm** — a probabilistic ranking model that weighs term frequency against document length. A `bool/should` query with custom boosts controls result order:

```
┌──────────────────────────────────────────────────────┐
│               RELEVANCE SCORING                      │
│                                                      │
│   Title  (exact match)    ──────────────  boost ×10  │  ← Highest
│   Title  (multi_match)    ──────────────  boost ×5   │
│   Author (multi_match)    ──────────────  boost ×2   │
│   Genre  (multi_match)    ──────────────  boost ×1   │
│   Description             ──────────────  boost ×1   │  ← Lowest
└──────────────────────────────────────────────────────┘
```

**Fuzziness (`AUTO`)** automatically allows:
- 1 character edit for words up to 5 characters
- 2 character edits for longer words

So `"harr poter"` → finds **Harry Potter** ✓

Each result exposes its `_score` from Elasticsearch, visible in the response JSON.

---

## ⚡ How Autocomplete Works

```
User types: "Har"
      │
      ▼
script.js  ──GET /autocomplete?q=Har──▶  Flask
                                              │
                              match_phrase_prefix query
                                              │
                                     Elasticsearch
                                              │
                         ["Harry Potter", "Haruki Murakami", ...]
                                              │
      ◀─────────────────── JSON response ─────┘
      │
Dropdown renders with matched text bolded:
  → [ **Har**ry Potter          ]
  → [ **Har**uki Murakami       ]
```

The frontend uses a **regex replace** to bold the matched prefix in each suggestion, giving users instant visual confirmation of what matched.

---

## 📡 API Reference

| Method | Endpoint | Query Param | Description |
|---|---|---|---|
| GET | `/` | — | API status check |
| GET | `/search` | `q` (string) | Full-text fuzzy search, returns ranked results |
| GET | `/autocomplete` | `q` (string) | Prefix-based live title suggestions |
| GET | `/count` | — | Total number of indexed documents |

**Example request:**
```
GET http://127.0.0.1:5000/search?q=harry+potter
```

**Example response:**
```json
[
  {
    "title": "Harry Potter and the Sorcerer's Stone",
    "author": "J.K. Rowling",
    "genre": "Fantasy",
    "description": "...",
    "rating": 4.47,
    "thumbnail": "https://...",
    "score": 38.21
  }
]
```

---

## 📂 Project Structure

```
book-search-engine/
│
├── app.py              # Flask API — all search and autocomplete endpoints
├── load_books.py       # Data pipeline — reads CSV and indexes into Elasticsearch
│
├── index.html          # Frontend UI — search bar, suggestions, result cards
├── style.css           # Responsive styles with CSS flexbox
├── script.js           # Async fetch, autocomplete logic, DOM rendering
│
├── data/
│   └── Books.csv       # Dataset (download separately — see below)
│
├── .env                # Your credentials — NEVER commit this file
├── .env.example        # Safe template — commit this instead]
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 
- Elasticsearch — [download](https://www.elastic.co/downloads/elasticsearch)

---

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/book_search_engine.git
cd book_search_engine
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install Python dependencies

```bash
pip install flask
pip install flask-cors
pip install elasticsearch
pip install pandas
pip install python-dotenv
 
```

### 4. Configure your credentials

```bash
cp .env.example .env
```

Open `.env` and fill in your Elasticsearch password:

```env
ES_HOST=https://localhost:9200
ES_USERNAME=elastic
ES_PASSWORD=your_password_here
ES_INDEX=search_engine
```

### 5. Start Elasticsearch

```bash
# macOS / Linux
./bin/elasticsearch

# Windows
.\bin\elasticsearch.bat
```

Elasticsearch runs on `https://localhost:9200` by default.
Your password is printed once on first startup. To reset it:

```bash
./bin/elasticsearch-reset-password -u elastic
```

Verify it's running:
```bash
curl -k -u elastic:YOUR_PASSWORD https://localhost:9200
# Should return cluster info JSON
```

---

### 6. Add the dataset

Place `Books.csv` inside the `data/` folder. The file should have these columns:

```
title, author, genre, description, publisher, language, average_rating, thumbnail
```

### 7. Index the data

```bash
python load_books.py
```

Expected output:
```
Connected: True
Books Indexed Successfully!
```

### 8. Start the Flask server

```bash
python app.py
```

### 9. Open the app

Open `index.html` in your browser and start searching.

---

## 🔮 Future Improvements

- [ ] **Pagination** — `from`/`size` parameters for navigating large result sets
- [ ] **Faceted filters** — filter by genre, language, and rating using ES aggregations
- [ ] **Docker Compose** — single command to start Elasticsearch + Flask together
- [ ] **Semantic search** — dense vector `knn` queries using sentence-transformers
- [ ] **Search analytics** — log queries to track popular searches and zero-result rates
- [ ] **Live deployment** — host on Render or Railway with a public URL

---

## 💡 Skills Demonstrated

```
Information Retrieval   →  BM25 ranking, fuzzy matching, field boosting, prefix queries
Backend Engineering     →  REST API design, environment-based config, input validation
Data Engineering        →  CSV ingestion, schema-aware indexing, pandas pipeline
Frontend Development    →  async/await, fetch API, live DOM updates, responsive CSS
Systems Thinking        →  end-to-end ownership from raw data to rendered search results
```

---


<div align="center">

Made with ☕ and Python

⭐ Star this repo if you found it useful!

</div>
