# Segment README Template

Copy this template for each of the remaining segments (S2, S3, S5-S10).

## Segment Structure

Each segment directory should have:

```
sX-segment-name/
├── README.md              # This file - segment overview and requirements
├── entries.jsonl          # Knowledge base entries (60-100 required)
├── templates/             # Document templates (3 minimum)
│   ├── template1.jinja2
│   ├── template2.jinja2
│   └── template3.jinja2
├── eval_set.jsonl         # 100 evaluation questions
└── testing_report.md      # User testing findings
```

## Knowledge Pack Topics

### Core Topics (adapt for your segment)

1. **Legal Framework** (15 entries)
   - Key acts and sections
   - Recent amendments
   - Supreme Court/High Court judgments
   - State-specific variations

2. **Common Issues** (20 entries)
   - Most frequent problems users face
   - Real-world scenarios
   - Edge cases
   - Misconceptions to address

3. **Procedures** (15 entries)
   - Step-by-step guides
   - Required documents
   - Filing processes
   - Timelines and deadlines

4. **Remedies & Solutions** (10 entries)
   - Available legal remedies
   - Government schemes
   - Free legal aid options
   - Alternative dispute resolution

5. **Portals & Helplines** (5 entries)
   - Government portals
   - Helpline numbers
   - Online filing procedures
   - Grievance redressal

6. **Special Considerations** (10 entries)
   - State-specific rules
   - Cost implications
   - Language/accessibility
   - Privacy/safety concerns

## Entry Format

```jsonl
{
  "content": "Detailed, accurate legal information in simple language (8th-grade reading level). Include examples where helpful. Cite the source law/section.",
  "metadata": {
    "act": "Name of Act/Law",
    "section": "Section number or 'General'",
    "topic": "Categorization (jurisdiction/procedure/remedy/etc.)",
    "state": "State code (DL/MH/KA) or 'All India'",
    "last_verified": "YYYY-MM-DD",
    "source_url": "https://indiacode.nic.in/... or official source",
    "language": "en",
    "tags": ["tag1", "tag2"]
  }
}
```

## Document Templates Required

Choose 3 most useful templates for your segment:
- Legal notice
- Complaint/petition
- Application
- Agreement
- Affidavit
- Checklist
- Appeal

Use Jinja2 templating. Variables should be clearly named.

## Wizards/Calculators Required (2 minimum)

Examples:
- Jurisdiction finder
- Limitation period calculator
- Eligibility checker
- Fee calculator
- Timeline estimator
- Document checklist generator

## Evaluation Questions

Create `eval_set.jsonl` with 100 questions:
- 50+ in English
- 50+ in Hindi or a regional language relevant to your segment
- Cover all major topics
- Include edge cases
- Mix of simple and complex queries

Format:
```jsonl
{
  "question": "User question",
  "language": "en",
  "segment": "s1-consumer",
  "expected_topics": ["topic1", "topic2"],
  "expected_contains": ["must contain this phrase", "and this"],
  "should_mention": ["helpline", "portal"],
  "difficulty": "easy/medium/hard"
}
```

## Testing Protocol

Test with **5+ real users** who match your segment's personas:
1. Give them 3-5 realistic scenarios
2. Let them use LegalBot to find answers
3. Observe without helping
4. Ask:
   - Did you get the information you needed?
   - Was it accurate and clear?
   - What would you do next?
   - What was confusing?
5. Document findings in `testing_report.md`

## Success Criteria

- ✅ 60-100 verified entries with sources
- ✅ All entries verified within last 6 months
- ✅ 3+ document templates working
- ✅ 2+ wizards/calculators functional
- ✅ 100 eval questions with verified answers
- ✅ 90%+ retrieval hit rate on eval set
- ✅ Zero fabricated section numbers
- ✅ 5+ real users successfully complete a journey
- ✅ All state-specific entries properly tagged

## Resources for Your Segment

List relevant:
- Government websites
- Legal databases
- Helpline numbers
- Portal URLs
- NGO/legal aid contacts
- Reference books/guides

## Timeline

- **Week 1-2**: Research, outline topics, meet users
- **Week 3-6**: Create 40+ entries, basic templates
- **Week 7-10**: Complete 60+ entries, wizards, Hindi
- **Week 11-13**: Reach 80-100, polish, test with users
- **Week 14-16**: Bug fixes, demo prep

## Notes for Your Segment

[Add segment-specific considerations]

- Special legal complexities?
- Emergency/safety considerations?
- Vulnerable user groups?
- Language needs?
- State variations?
- Recent law changes?
