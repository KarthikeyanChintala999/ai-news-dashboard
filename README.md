# 🧠 AI News Aggregation & Broadcasting Dashboard

An end-to-end AI-powered system that aggregates, processes, and broadcasts the latest AI news from multiple sources using asynchronous pipelines, LLM summarization, and semantic embeddings.

---

## 🚀 Overview

This project implements a scalable backend system that:

- Collects AI-related news from multiple RSS sources
- Processes and deduplicates articles
- Generates summaries using LLMs
- Stores structured news data in PostgreSQL
- Broadcasts curated news via Telegram

The system is designed using a **worker-based asynchronous architecture** to simulate real-world production pipelines.

---

## 🧩 System Architecture


[RSS Sources]
↓
[Ingestion Worker]
↓
[Raw Articles DB]
↓
[Processing Worker (LLM + Embeddings)]
↓
[News Items DB]
↓
[Scheduler]
↓
[Telegram Broadcast]


---

## ⚙️ Features

### 📰 News Ingestion
- RSS-based ingestion using `feedparser`
- Supports multiple sources (OpenAI, HackerNews, arXiv, etc.)
- Deduplication using URL hashing

### 🧠 AI Processing
- LLM-based summarization (Groq API)
- Fallback mechanism for robustness
- Semantic embeddings using Sentence Transformers (MiniLM)

### 🔍 Deduplication
- URL-level deduplication
- Prevents duplicate entries in processed news

### 📊 Data Storage
- PostgreSQL with async SQLAlchemy
- Structured schema:
  - `sources`
  - `raw_articles`
  - `news_items`
  - `favorites`
  - `broadcast_logs`
  - `users`

### 📣 Broadcasting
- Telegram bot integration
- Automated newsletter generation
- Periodic scheduling using async workers

---

## 🛠️ Tech Stack

| Layer        | Technology |
|-------------|-----------|
| Backend     | FastAPI |
| Database    | PostgreSQL |
| ORM         | SQLAlchemy (Async) |
| AI Models   | Groq LLM, Sentence Transformers |
| Ingestion   | Feedparser |
| Workers     | AsyncIO |
| Deployment  | Uvicorn |

---

## 📂 Project Structure


backend/
│
├── app/
│ ├── ingestion/ # RSS ingestion + scheduler
│ ├── processing/ # summarization + embeddings
│ ├── clustering/ # clustering (optional)
│ ├── newsletter/ # newsletter generation
│ ├── bot/ # telegram integration
│ ├── models/ # database models
│ ├── database.py
│ ├── config.py
│ └── main.py
│
├── requirements.txt
└── README.md


---

## ⚡ How to Run

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/ai-news-dashboard.git
cd ai-news-dashboard/backend
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Setup environment variables

Create a .env file:

DATABASE_URL=your_postgres_url
GROQ_API_KEY=your_groq_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
4️⃣ Run the server
uvicorn app.main:app --reload --port 8001
🔄 Background Workers

The system automatically starts:

📡 Ingestion Worker → Fetches RSS feeds

🧠 Processing Worker → Generates summaries & embeddings

🧩 Clustering Worker → Groups similar news (optional)

📰 Newsletter Worker → Sends updates via Telegram

🧠 Key Design Decisions

Async-first architecture for scalability

Separation of raw vs processed data

LLM fallback handling to avoid pipeline failures

Batch processing with transaction safety

Embedding-based representation for future clustering/search

⚠️ Known Limitations

Summarization may fallback to title if API fails

Clustering is basic (can be improved using vector DB)

Frontend dashboard not implemented (backend-focused MVP)

🚀 Future Improvements

Add React dashboard (news feed + favorites)

Integrate Redis queue (Celery / RQ)

Advanced clustering using pgvector / FAISS

Better ranking (impact scoring)

Multi-platform broadcasting (Email, LinkedIn, WhatsApp)

📬 Example Output (Telegram)
🧠 AI Daily Digest

🔥 Show HN: Antfly...

Summary of the article...

Read more:
https://...

🔥 Microsoft Xbox hacked...

Summary...

Read more:
https://...
👨‍💻 Author

Karthikeyan Srinivas Chintala

🏁 Conclusion

This project demonstrates:

Real-world backend system design

AI integration into data pipelines

Asynchronous processing architecture

Scalable and modular engineering practices