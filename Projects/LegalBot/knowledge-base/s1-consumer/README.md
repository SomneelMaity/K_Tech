# Segment 1: Consumer Protection & E-commerce

## Overview
Consumer rights, defective products, refunds, e-commerce disputes, builder delays, insurance claims

**Key Laws:** Consumer Protection Act 2019, e-Jagriti Portal, NCH 1915  
**Difficulty:** Easy-Medium

## Knowledge Pack (60-100 entries required)

This directory will contain:

### 1. entries.jsonl
Each line is a JSON object with:
```json
{
  "content": "Text content with legal information",
  "metadata": {
    "act": "Consumer Protection Act 2019",
    "section": "Section 35",
    "topic": "District Commission Jurisdiction",
    "state": "All India",
    "last_verified": "2026-01-15",
    "source_url": "https://indiacode.nic.in/...",
    "language": "en"
  }
}
```

### 2. Topics to Cover (minimum 60 entries)

#### A. Consumer Forums & Jurisdiction (10 entries)
- District Commission (up to ₹1 crore)
- State Commission (₹1 crore - ₹10 crore)
- National Commission (>₹10 crore)
- e-Jagriti online filing process
- Zero fee for claims up to ₹5 lakh
- 2-year limitation period
- No lawyer needed for filing

#### B. Common Disputes (15 entries)
- Defective products
- Service deficiency
- Unfair trade practices
- E-commerce refund delays
- Wrong product delivered
- Builder delays (RERA)
- Insurance claim rejection
- Coaching fee disputes

#### C. Filing Process (10 entries)
- How to draft a complaint
- Evidence checklist
- Legal notice template
- Online filing walkthrough
- Offline filing procedure
- Complaint format
- Consumer court fees

#### D. Remedies Available (8 entries)
- Replacement of goods
- Refund with interest
- Compensation for deficiency
- Damages for mental agony
- Punitive damages

#### E. E-commerce Specific (12 entries)
- Consumer Rights (replacement, refund, warranty)
- Grievance redressal mechanism
- Consumer Protection (E-Commerce) Rules 2020
- How to escalate to platform
- How to file complaint against platform
- Jurisdictional issues in online sales

#### F. Sector-Specific (5 entries each = 25 total)
- Banking & Finance
- Insurance
- Real Estate (RERA)
- Telecom
- Airlines

## Document Templates (3 required)

1. **Legal Notice** - Demand for refund/replacement
2. **Consumer Complaint** - To District/State/National Commission
3. **e-Jagriti Form** - Online complaint filing

## Wizards/Calculators (2 required)

1. **Forum Finder** - Input amount in dispute → suggests correct forum
2. **Limitation Calculator** - Input date of purchase/service → days remaining to file

## Evaluation Set (100 questions in 2+ languages)

Sample questions:
- "I bought a defective phone, what can I do?" (English)
- "मुझे ऑनलाइन ऑर्डर में गलत प्रोडक्ट मिला, कैसे शिकायत करूं?" (Hindi)
- "Builder has delayed possession by 2 years, where to complain?"
- "E-commerce site is not refunding my money for 4 months"

## Team Roles (4 students)

1. **Legal Researcher/Content Lead**: Create 60-100 knowledge entries
2. **Backend RAG Engineer**: Implement retrieval & ingestion
3. **Frontend/Conversation Designer**: Build consumer segment UI
4. **QA & Evaluation Lead**: Test with 5+ real users, measure accuracy

## Key Portals & Helplines

- **e-Jagriti Portal**: https://jagriti.gov.in
- **Consumer Helpline**: 1915
- **NCH Website**: https://consumerhelpline.gov.in
- **Sector Ombudsmen**: RBI, IRDAI, TRAI

## Success Metrics

- 90%+ retrieval hit rate on evaluation questions
- Zero fabricated section numbers/acts
- Correct forum identification for all test cases
- 5+ real users successfully draft a complaint
