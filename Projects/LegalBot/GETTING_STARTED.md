# LegalBot - Getting Started Guide

## Quick Start (5 minutes)

### Prerequisites
- **Backend**: Python 3.10+, pip
- **Frontend**: Node.js 18+, npm
- **Optional**: Docker & Docker Compose

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone <repo-url>
cd LegalBot

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Edit backend/.env and add your API keys:
# - LLM_API_KEY (OpenAI or Anthropic)
# - BHASHINI_API_KEY (optional, for translation)

# Start all services
docker-compose up

# Access:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit .env
cp .env.example .env
# Add your LLM_API_KEY

# Run server
uvicorn app.main:app --reload

# Access API docs: http://localhost:8000/docs
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy and edit .env.local
cp .env.local.example .env.local

# Run development server
npm run dev

# Access: http://localhost:3000
```

## For Segment Teams

### 1. Choose Your Segment

You'll be assigned one of these 10 segments:

- **S1**: Consumer & E-commerce
- **S2**: Property, Land & Tenancy
- **S3**: Family Law & Maintenance
- **S4**: Cyber Crime Response ⚠️ (Emergency-critical)
- **S5**: Employment & Labour
- **S6**: Police, FIR & Bail
- **S7**: Women & Child Safety ⚠️ (Emergency-critical)
- **S8**: Senior Citizens
- **S9**: RTI & Govt Services
- **S10**: MSME & Small Business

### 2. Set Up Your Workspace

```bash
# Create your team's branch
git checkout -b segment/s1-consumer

# Your segment directory
cd knowledge-base/s1-consumer
# Read README.md for segment requirements
```

### 3. Team Roles & Responsibilities

**👨‍⚖️ Legal Researcher / Content Lead**
```bash
# Your job: Create 60-100 verified knowledge entries
cd knowledge-base/s1-consumer

# Create entries.jsonl
# Format: one JSON object per line
# See README.md for schema

# Example entry:
{"content": "Consumer Protection Act 2019 establishes...", "metadata": {"act": "CPA 2019", "section": "35", ...}}
```

**🔧 Backend RAG Engineer**
```bash
cd backend

# Create segment module
mkdir -p app/segments/s1_consumer
cd app/segments/s1_consumer

# Create files:
# - __init__.py
# - queries.py (segment-specific handling)
# - calculators.py (wizards/calculators)
# - templates.py (document templates)

# Ingest your knowledge base
python scripts/ingest/ingest_kb.py --segment s1-consumer
```

**🎨 Frontend / Conversation Designer**
```bash
cd frontend

# Create segment components
mkdir -p src/components/segments/s1-consumer

# Create:
# - IntakeForm.tsx (≤6 questions)
# - Wizards.tsx (calculators)
# - DocumentGenerator.tsx
```

**✅ QA & Evaluation Lead**
```bash
# Create evaluation set
cd knowledge-base/s1-consumer

# Create eval_set.jsonl
# 100 questions in 2+ languages
# Format:
{"question": "How do I file consumer complaint?", "language": "en", "expected_contains": ["District Commission", "e-Jagriti"]}

# Test with real users (minimum 5)
# Document findings in testing_report.md
```

### 4. Development Cycle

**Week 1-2: Foundation**
- Read your segment README thoroughly
- Research laws, portals, helplines
- Meet 2-3 real users or legal aid workers
- Outline knowledge pack topics

**Week 3-6: Build Knowledge Pack v1**
- Content Lead: Create 40+ entries
- Backend: Set up ingestion pipeline
- Frontend: Basic intake form
- QA: Create 50 eval questions

**Week 7-10: Wizards & Documents**
- Content Lead: Complete 60+ entries, add Hindi
- Backend: Build calculators/wizards
- Frontend: Polish UI, add document generation
- QA: Complete 100 eval questions, test with 3 users

**Week 11-13: Test & Polish**
- Content Lead: Reach 80+ entries, verify all sources
- Backend: Optimize retrieval, add state filters
- Frontend: Accessibility, mobile testing
- QA: Test with 5+ users, measure accuracy

**Week 14-16: Demo Prep**
- All: Bug fixes from testing
- All: Prepare demo script
- All: Practice live persona journey
- All: Write final documentation

## Testing Your Work

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Query endpoint
curl -X POST http://localhost:8000/api/v1/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I file a consumer complaint?",
    "segment": "s1-consumer",
    "language": "en"
  }'
```

### Test Knowledge Base

```bash
cd backend

# Verify entries are valid JSON
python scripts/validate_kb.py --segment s1-consumer

# Test retrieval
python scripts/test_retrieval.py \
  --segment s1-consumer \
  --query "consumer forum jurisdiction"
```

### Test Frontend

```bash
cd frontend

# Type check
npm run type-check

# Lint
npm run lint

# Build (catches errors)
npm run build
```

## Common Issues & Solutions

### Backend won't start

```
Error: ModuleNotFoundError: No module named 'app'
```
**Solution**: Make sure you're in `backend/` directory and venv is activated.

```
Error: LLM_API_KEY not set
```
**Solution**: Copy `.env.example` to `.env` and add your API key.

### Frontend build fails

```
Error: Module not found: Can't resolve '@/components/...'
```
**Solution**: Check `tsconfig.json` paths are correct, restart dev server.

### Knowledge base not loading

```
Warning: No entries file found for s1-consumer
```
**Solution**: Create `knowledge-base/s1-consumer/entries.jsonl` with at least one entry.

### RAG returns "I don't have enough information"

**Solution**: 
1. Check if your knowledge base is ingested: `python scripts/verify_kb.py`
2. Lower similarity threshold in query
3. Add more varied entries to cover edge cases

## Next Steps

- **Read**: [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
- **Explore**: Your segment's `knowledge-base/[segment]/README.md`
- **Join**: Slack channel for your segment
- **Ask**: Mentor or platform team if stuck

## Resources

- **Legal Databases**: 
  - https://indiacode.nic.in (Statutes)
  - https://egazette.gov.in (Notifications)
  - https://nalsa.gov.in (Legal Aid)

- **APIs**:
  - FastAPI Docs: http://localhost:8000/docs
  - Next.js Docs: https://nextjs.org/docs

- **Design**:
  - Personas: See project document
  - Accessibility: WCAG AA minimum

---

**Ready to build?** Choose your segment, read its README, and start creating! 🚀
