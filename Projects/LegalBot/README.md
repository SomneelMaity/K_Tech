# LegalBot - AI-Powered Legal Assistant for India

> **Vision**: A free, multilingual, voice-enabled assistant that helps Indians understand their legal rights, navigate the justice system, and access free legal aid.

## 🎯 Project Overview

LegalBot breaks the chain of legal confusion → fear → wrong steps → money lost → giving up. It provides:
- **Multilingual Support**: 10+ Indian languages (text & voice)
- **10 Legal Domains**: Consumer rights, property, family law, cybercrime, employment, police/FIR, women & child safety, senior citizens, RTI, and MSME
- **RAG Architecture**: Retrieval-Augmented Generation for verified, cited legal information
- **Document Generation**: Notices, complaints, RTI applications, agreements
- **Free Legal Aid Routing**: NALSA/DLSA, Tele-Law, helplines (1930/181/1098/14567/1915)

## 📊 The Problem

- **5.39 crore+** pending cases (Dec 2025)
- **~85%** in district courts, 1.8 lakh cases pending >30 years
- **~15%** rural awareness of free legal aid (NALSA 2022)
- **₹2,700-2,800/day** litigant costs including lost income
- **~21 judges/million** vs 50 recommended

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js PWA)                │
│  • WhatsApp Business API Channel                        │
│  • Voice (Bhashini ASR/TTS, Web Speech API)            │
│  • Multilingual UI                                       │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│              Backend API (Python FastAPI)                │
│  • RAG Service (Query → Retrieve → Generate)            │
│  • Language Service (Translation, Detection)            │
│  • Document Generator (Jinja → PDF/DOCX)               │
│  • Safety Middleware (Emergency Detection)              │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                Knowledge Base (Vector DB)                │
│  • 10 Segment-Specific Knowledge Packs                  │
│  • Statutes, Rules, Portal Guides, FAQs                │
│  • Metadata: Act, Section, State, Date, BNS/BNSS       │
└─────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
LegalBot/
├── backend/               # Python FastAPI backend
│   ├── app/
│   │   ├── api/          # REST API endpoints
│   │   ├── core/         # RAG engine, config
│   │   ├── services/     # Language, doc-gen, safety
│   │   ├── models/       # Data models
│   │   └── segments/     # 10 segment modules
│   ├── tests/
│   └── requirements.txt
│
├── frontend/             # Next.js PWA frontend
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities, API client
│   │   └── segments/     # Segment-specific UI
│   └── package.json
│
├── knowledge-base/       # Legal content for RAG
│   ├── s1-consumer/      # Consumer & E-commerce
│   ├── s2-property/      # Property, Land & Tenancy
│   ├── s3-family/        # Family Law & Maintenance
│   ├── s4-cybercrime/    # Cyber Crime Response
│   ├── s5-employment/    # Employment & Labour
│   ├── s6-police/        # Police, FIR & Bail
│   ├── s7-women-child/   # Women & Child Safety
│   ├── s8-seniors/       # Senior Citizens
│   ├── s9-rti/           # RTI & Govt Services
│   └── s10-msme/         # MSME & Small Business
│
├── shared/               # Shared utilities
│   ├── schemas/          # Common data schemas
│   └── templates/        # Document templates
│
├── docs/                 # Documentation
│   ├── architecture/
│   ├── segments/         # Per-segment docs
│   └── deployment/
│
├── scripts/              # Automation scripts
│   ├── ingest/           # KB ingestion
│   └── evaluation/       # Testing & metrics
│
└── .github/
    └── workflows/        # CI/CD
```

## 🎓 10 Project Segments (10 Teams × 4 Students)

| # | Segment | Key Laws/Portals | Difficulty |
|---|---------|------------------|------------|
| S1 | Consumer & E-commerce | CPA 2019, e-Jagriti, NCH 1915 | Easy-Med |
| S2 | Property, Land & Tenancy | TPA, RERA, Rent Acts | Hard |
| S3 | Family Law & Maintenance | HMA, SMA, PWDVA, BNSS §144 | Hard |
| S4 | Cyber Crime Response | IT Act, BNS, NCRP 1930 | Medium |
| S5 | Employment & Labour | Wage Code, POSH, PF/ESI | Medium |
| S6 | Police, FIR & Bail | BNS, BNSS, BSA 2023 | Hard |
| S7 | Women & Child Safety | PWDVA, POSH, POCSO | Hard* |
| S8 | Senior Citizens | MWPSC 2007, Elder Line 14567 | Easy-Med |
| S9 | RTI & Govt Services | RTI Act 2005, MV Act | Easy |
| S10 | MSME & Small Business | MSMED, Samadhaan, NI §138 | Medium |

### Common Deliverables (Every Team)

1. **Knowledge Pack**: 60-100 verified entries (state-tagged, source-cited)
2. **Conversation Design**: Intake flow + 2+ wizards/calculators
3. **Document Templates**: 3+ generator templates (notices, complaints, etc.)
4. **Evaluation Set**: 100 questions in 2+ languages with verified answers
5. **User Testing**: 5+ real users matching personas

### Team Roles (4 per segment)

1. **Legal Researcher / Content Lead**: Create knowledge pack
2. **Backend RAG Engineer**: Implement retrieval & generation
3. **Frontend / Conversation Designer**: Build segment UI & flows
4. **QA & Evaluation Lead**: Test with real users, measure accuracy

## 🚀 Getting Started

### Prerequisites

- **Backend**: Python 3.10+, pip
- **Frontend**: Node.js 18+, npm/yarn
- **Database**: PostgreSQL (optional), FAISS/ChromaDB for vectors
- **APIs**: 
  - LLM API (OpenAI/Anthropic/local)
  - Bhashini API (GoI) for translation
  - WhatsApp Business API (optional)

### Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repo-url>
   cd LegalBot
   ```

2. **Backend setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API keys
   uvicorn app.main:app --reload
   ```

3. **Frontend setup**:
   ```bash
   cd frontend
   npm install
   cp .env.local.example .env.local
   # Edit .env.local with backend URL
   npm run dev
   ```

4. **Ingest Knowledge Base**:
   ```bash
   cd backend
   python scripts/ingest/ingest_kb.py --segment s1-consumer
   ```

## 📚 Documentation

- [Architecture Overview](docs/architecture/README.md)
- [RAG System Design](docs/architecture/rag-design.md)
- [Segment Guide Template](docs/segments/SEGMENT_TEMPLATE.md)
- [API Documentation](docs/api/README.md)
- [Ethics & Legal Boundaries](docs/ethics.md)

## 🔒 Ethics & Legal Boundaries

- **Information, Not Advice**: Complies with Advocates Act 1961
- **Accuracy Discipline**: No fabricated section numbers, verified every 6 months
- **Privacy**: Minimal PII, encrypted, user-controlled deletion
- **Safety-First**: Emergency detection → helpline routing
- **Bias & Inclusion**: Equal quality across religions, genders, castes, states

## 📊 Evaluation & Grading

- **Accuracy** (30%): Correct forum/law/procedure, zero fabricated citations
- **Usefulness** (25%): Real users complete their journey
- **Safety & Ethics** (20%): Privacy, bias screening, emergency handling
- **Engineering** (15%): Code quality, tests, deployment
- **Content Craftsmanship** (10%): Multilingual quality, citations

## 📅 Roadmap

### Week 1-2: Foundation
- Domain deep-dive, meet 5 real users/aid workers
- Finalize scope, platform setup
- RAG skeleton, KB schema

### Week 3-6: Knowledge Packs v1
- 40+ cited entries per segment
- Retrieval end-to-end
- First flows, disclaimer & safety middleware live

### Week 7-10: Wizards & Documents
- Calculators, doc generators
- Hindi + 1 regional language
- WhatsApp pilot, cross-team red-teaming

### Week 11-13: Evaluation & Polish
- 100-question eval sets (>90% retrieval hit rate)
- Persona-matched user testing
- Fixes, polish

### Week 14-16: Demo Day
- Load test, live persona journeys
- Publish combined KB + eval report

## 🌐 Key Data Sources

- **Statutes**: [India Code](https://indiacode.nic.in)
- **Notifications**: [e-Gazette](https://egazette.gov.in)
- **Legal Aid**: [NALSA](https://nalsa.gov.in), [DoJ Tele-Law](https://doj.gov.in)
- **Consumer**: [Jagriti Portal](https://jagriti.gov.in), [NCH](https://consumerhelpline.gov.in)
- **Cybercrime**: [NCRP](https://cybercrime.gov.in)
- **MSME**: [Samadhaan](https://samadhaan.msme.gov.in)
- **Courts**: [NJDG](https://njdg.ecourts.gov.in)
- **Research**: [PRS India](https://prsindia.org), [DAKSH](https://dakshindia.org)

## 📝 License

[MIT License](LICENSE) - Free for educational and non-commercial use.

## 🤝 Contributing

This is a student project (10 teams × 4 students). Each segment team maintains their module independently. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📞 Support & Helplines Referenced

- **Cybercrime**: 1930
- **Women in Distress**: 181
- **Child Helpline**: 1098
- **Elder Line**: 14567
- **Consumer Helpline**: 1915
- **Legal Aid**: NALSA/DLSA (varies by state)

---

**Built with ❤️ to bridge India's justice gap, one conversation at a time.**
