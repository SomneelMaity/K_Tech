# LegalBot System

An AI-Powered Legal Assistant for Every Indian.

LegalBot is a free, multilingual, voice-enabled assistant that any Indian citizen can open the moment a legal problem strikes. It explains rights, options, next steps, required documents, and connects users to free government legal help.

## Active Segments

| ID | Domain | Status |
|----|--------|--------|
| S5 | Employment & Labour | In Development |
| S10 | MSME & Small Business | In Development |

## Project Structure

```
LegalBot_System/
├── platform/               # Shared core platform (chat shell, RAG, language, safety)
│   ├── backend/            # FastAPI backend — RAG service, doc-gen, safety middleware
│   └── frontend/           # React/Vite PWA — chat shell, shared UI components
├── segments/
│   ├── s5-employment/      # Segment 5: Employment & Labour
│   └── s10-msme/           # Segment 10: MSME & Small Business
├── knowledge-base/         # Curated RAG knowledge packs (per segment)
├── scripts/                # Utility scripts (validation, ingestion, evaluation)
├── docker-compose.yml
└── README.md
```

## Quick Start

### Backend
```sh
cd platform/backend
cp .env.example .env   # fill in API keys
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```sh
cd platform/frontend
npm install
npm run dev
```

## Architecture

LegalBot uses Retrieval-Augmented Generation (RAG): every answer is grounded in verified Indian legal provisions retrieved from the knowledge base before generation. The LLM writes plain-language answers strictly from retrieved text and must cite them.

- **Ingestion**: Statutes → clean → chunk per section with metadata → embed → vector DB
- **Query flow**: message → language detect → domain classification → safety check → hybrid retrieval → rerank → grounded answer with citations → translate + disclaimer
- **Guardrails**: Refuse out-of-scope; mandatory disclaimer; emergency router; "I don't know" on low confidence — never guess a section number

## Ethics & Legal Boundaries

LegalBot provides **general legal information**, not legal advice. It shows a disclaimer on every session and document, and routes high-stakes matters to free human lawyers (NALSA/DLSA/Tele-Law). See [ETHICS.md](ETHICS.md) for full policy.
