# Faceless UGC Factory

Turn an idea or product description into a ready-to-post **caption + image** in
seconds. This is **Pipeline 1 (Content-to-Post)** — the first vertical slice of
the larger faceless-UGC platform.

```
idea → angle & audience → hook + caption + hashtags → styled image → review/edit → download
```

- **Backend:** FastAPI + SQLAlchemy (SQLite)
- **Frontend:** React + Vite + Tailwind
- **AI:** Claude (`claude-opus-4-8`) for copy · Pollinations (free, default) / Flux / Gemini for images

It runs out of the box in **demo mode** (placeholder copy + image) so you can
click through the whole flow before adding any API keys.

## Quick start

### 1. Backend

```bash
cd backend
cp .env.example .env          # add ANTHROPIC_API_KEY + REPLICATE_API_TOKEN (optional)
.venv/bin/uvicorn app.main:app --reload --port 8000
```

(The virtualenv at `backend/.venv` already has the dependencies installed. To
recreate it: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.)

API docs at http://localhost:8000/docs · health at http://localhost:8000/api/health

### 2. Frontend

```bash
cd frontend
npm run dev
```

Open http://localhost:5173. The dev server proxies `/api` and `/storage` to the
backend on port 8000.

## Keys

| Variable | What it powers | Get it from |
|---|---|---|
| `ANTHROPIC_API_KEY` | Caption / hook / hashtag generation | https://console.anthropic.com |
| `REPLICATE_API_TOKEN` | Flux image generation (paid, optional) | https://replicate.com/account |
| `GEMINI_API_KEY` | Image generation (needs billing, optional) | https://aistudio.google.com/apikey |

**Images are free out of the box** via Pollinations (`IMAGE_PROVIDER=pollinations`)
— no key required. The keys above are optional paid upgrades: set
`REPLICATE_API_TOKEN` and `IMAGE_PROVIDER=replicate`, or `GEMINI_API_KEY` and
`IMAGE_PROVIDER=gemini` (Gemini image gen requires billing — the free tier is
text-only).

## What's next (roadmap)

This slice deliberately stops at **generate + download**. The shared "spine" it
establishes (generation service, asset storage, library, usage tracking) is
reused by later pipelines:

- **P1b/c** — connect social accounts, schedule, and auto-publish (IG/FB/Threads)
- **P2** — faceless video (script → voiceover → avatar/animation → captions)
- **P4** — analytics feedback loop (optimal times, A/B, what hooks work)
- **P3** — ads & campaigns · **P5** — leads & follow-up
