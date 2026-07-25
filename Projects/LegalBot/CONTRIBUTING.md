# LegalBot - Contributing Guide

Thank you for contributing to LegalBot! This project is divided into 10 segments, each managed by a separate team.

## Project Structure

```
10 Segments × 4 Team Members = 40 Students Total
```

Each team is responsible for one legal domain (S1-S10).

## Team Composition (4 members per segment)

1. **Legal Researcher / Content Lead**
   - Create 60-100 verified knowledge entries
   - Ensure accurate citations (act, section, state, date)
   - Re-verify every 6 months
   
2. **Backend RAG Engineer**
   - Implement segment-specific retrieval logic
   - Create embeddings and ingest knowledge base
   - Build calculators/wizards
   
3. **Frontend / Conversation Designer**
   - Design segment-specific UI flows
   - Create intake forms (≤6 questions)
   - Build document generation interface
   
4. **QA & Evaluation Lead**
   - Create 100-question evaluation set (2+ languages)
   - Test with 5+ persona-matched real users
   - Measure accuracy, safety, usability
   - Report bugs and edge cases

## Development Workflow

### 1. Knowledge Pack Creation

Each segment needs **60-100 entries** in `knowledge-base/[segment-id]/entries.jsonl`:

```jsonl
{"content": "Section 35 of Consumer Protection Act 2019 establishes District Consumer Disputes Redressal Commissions with jurisdiction to entertain complaints where the value of goods or services and compensation claimed does not exceed rupees one crore.", "metadata": {"act": "Consumer Protection Act 2019", "section": "35", "topic": "Jurisdiction", "state": "All India", "last_verified": "2026-01-15", "source_url": "https://indiacode.nic.in/...", "language": "en"}}
```

**Requirements:**
- Every entry MUST have a verified source
- Include state if law is state-specific
- Update `last_verified` date
- Tag with appropriate metadata

### 2. Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit environment file
cp .env.example .env
# Edit .env with your API keys

# Run development server
uvicorn app.main:app --reload
```

**Adding a segment module:**
```python
# backend/app/segments/s1_consumer/
# - __init__.py
# - queries.py (segment-specific query handling)
# - calculators.py (forum finder, limitation calc, etc.)
# - templates.py (document templates)
```

### 3. Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Copy and edit environment file
cp .env.local.example .env.local

# Run development server
npm run dev
```

**Adding segment UI:**
```tsx
// frontend/src/components/segments/s1-consumer/
// - ConsumerIntakeForm.tsx
// - ForumFinder.tsx
// - ComplaintGenerator.tsx
```

### 4. Knowledge Base Ingestion

```bash
cd backend

# Ingest a segment's knowledge base
python scripts/ingest/ingest_kb.py --segment s1-consumer

# Verify ingestion
python scripts/ingest/verify_kb.py --segment s1-consumer
```

## Deliverables Checklist

### Every Team Must Submit:

- [ ] **Knowledge Pack** (60-100 entries)
  - [ ] All entries have verified sources
  - [ ] State-specific entries are tagged
  - [ ] Last verified date within 6 months
  
- [ ] **Conversation Design**
  - [ ] Intake flow (≤6 questions)
  - [ ] At least 2 wizards/calculators
  - [ ] Domain-specific tone guide
  
- [ ] **Document Templates** (minimum 3)
  - [ ] Validated against real formats
  - [ ] Support Hindi + English
  - [ ] Include fill-in-the-blank fields
  
- [ ] **Evaluation Set** (100 questions)
  - [ ] 50+ in English
  - [ ] 50+ in Hindi or regional language
  - [ ] Verified ideal answers
  - [ ] Edge cases covered
  
- [ ] **User Testing**
  - [ ] 5+ real users matching personas
  - [ ] Test report with findings
  - [ ] Bug fixes based on feedback

## Code Quality Standards

### Python (Backend)
- Type hints for all functions
- Docstrings for public APIs
- pytest for unit tests
- Black for formatting
- No hardcoded secrets

### TypeScript (Frontend)
- Strict TypeScript mode
- Component documentation
- Accessibility (WCAG AA)
- Mobile-first responsive design
- ESLint compliance

### Knowledge Entries
- Cite source URL or legal text reference
- Use 8th-grade reading level language
- Include examples where helpful
- State limitations clearly ("This applies only in Maharashtra")

## Testing Requirements

### Accuracy Testing (30% of grade)
- **Zero fabricated citations** - Every section number, act name, deadline MUST be in KB
- Correct forum/commission for all test cases
- No contradictory information
- State-specific vs All-India correctly distinguished

### Usefulness Testing (25% of grade)
- Real user completes journey (question → answer → next steps → document)
- ≥90% retrieval hit rate on eval questions
- Average response time <5 seconds
- Users report "this helped me understand what to do"

### Safety & Ethics Testing (20% of grade)
- Emergency detection working (for S4, S7, S6)
- No harmful advice
- Privacy preserved (no PII leakage)
- Disclaimer always shown
- Helplines surfaced correctly

## Git Workflow

```bash
# Create feature branch
git checkout -b segment/s1-consumer/feature-name

# Make changes
git add .
git commit -m "S1: Add consumer forum jurisdiction entries"

# Push and create PR
git push origin segment/s1-consumer/feature-name
```

**Branch naming:**
- `segment/s1-consumer/*` - Consumer team
- `segment/s4-cybercrime/*` - Cybercrime team
- `platform/*` - Platform team (shared services)
- `docs/*` - Documentation

**Commit messages:**
- Prefix with segment: `S1:`, `S4:`, `Platform:`
- Be descriptive: `S4: Add golden hour wizard for fraud victims`

## Code Review Process

1. All PRs require review from:
   - One teammate
   - Platform team (for API changes)
   
2. Checklist:
   - [ ] Tests pass
   - [ ] No hardcoded values
   - [ ] Documentation updated
   - [ ] Knowledge entries have sources
   - [ ] No breaking changes to other segments

## Communication

- **Slack channels:**
  - #s1-consumer through #s10-msme (segment teams)
  - #platform (shared services)
  - #qa-testing (cross-team testing)
  
- **Weekly sync:** Every Friday 5 PM
- **Demo days:** End of weeks 6, 10, 13, 16

## Resources

- **Legal databases:** indiacode.nic.in, egazette.gov.in, nalsa.gov.in
- **Design system:** Figma link [TBD]
- **API docs:** `/docs` endpoint on backend
- **Project tracker:** GitHub Projects

## Questions?

Contact:
- Platform team: platform@legalbot.team
- Your segment mentor: [assigned at kickoff]

---

**Remember:** Accuracy > Speed. One fabricated section number fails the entire eval.
