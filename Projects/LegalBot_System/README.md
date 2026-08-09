# LegalBot System

AI-powered legal information assistant for Indian citizens, built with RAG (ChromaDB + Google Gemini). Covers **Employment & Labour (S5)** and **MSME & Small Business (S10)** law across 36 curated knowledge entries with support for 10 Indian languages.

## Stack

- **Backend**: FastAPI · ChromaDB · Google Gemini (`gemini-flash-latest`) · SQLite
- **Frontend**: React 19 · Vite · Tailwind CSS
- **Other**: `langdetect` · `deep-translator` · `xhtml2pdf`

## Quick Start

**Backend**
```sh
cd platform/backend
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
# Add GEMINI_API_KEY to .env
uvicorn app.main:app --reload
```

**Frontend**
```sh
cd platform/frontend
npm install && npm run dev
```

Backend → http://localhost:8000 · Frontend → http://localhost:5173

## Key Environment Variables

| Variable | Default |
|----------|---------|
| `GEMINI_API_KEY` | *(required)* |
| `CHAT_MODEL` | `gemini-flash-latest` |
| `DATABASE_URL` | `sqlite:///./legalbot.db` |
| `CORS_ORIGINS` | `http://localhost:5173` |

> LegalBot provides general legal information only — not legal advice. Free legal aid: NALSA **1516**.
