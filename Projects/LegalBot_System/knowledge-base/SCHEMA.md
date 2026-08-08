# Knowledge Base — Schema & Guidelines

## Entry Format (YAML front-matter + Markdown body)

Every KB entry is a Markdown file with YAML front-matter:

```yaml
---
entry_id: s5-001                   # segment prefix + sequential number
segment: s5-employment             # s5-employment | s10-msme
title: "Gratuity — Eligibility and Calculation"
act: "Payment of Gratuity Act 1972"
section: "Section 4"
state: all                         # "all" or ISO state code e.g. "MH", "KA"
language: en
last_verified: "2026-07"
source_url: "https://indiacode.nic.in/handle/123456789/2001"
tags: [gratuity, salary, termination, retirement]
---
```

## Body (Markdown, 8th-grade reading level)

- Write in plain language — avoid "legalese"
- State the right / rule, then the exact number / threshold
- Cite the specific section
- Mention the forum / how to enforce
- Note any state variation
- End with a "What to do" bullet list

## Quality Rules

1. Every section number MUST be verified against the source URL
2. Monetary thresholds, timelines, and percentages MUST be double-checked
3. Mark BNS/BNSS section numbers explicitly where IPC/CrPC equivalents exist
4. Re-verify every entry at least every 6 months; update `last_verified`
5. Do NOT copy-paste legal text wholesale — paraphrase to 8th-grade level
6. For state-specific rules, create one entry per state (or note all states that differ)
