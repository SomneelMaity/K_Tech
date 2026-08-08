# S5 Employment & Labour — Conversation Flow Design

## Intake Flow (≤ 6 questions)

```
Q1. What is your employment situation?
    [ ] Formal / salaried employee
    [ ] Gig / freelance / platform worker
    [ ] Domestic worker
    [ ] Contract / daily-wage worker
    [ ] I am an employer

Q2. What is the problem you are facing?
    [ ] Salary not paid / delayed
    [ ] PF / ESI not deposited
    [ ] Gratuity denied
    [ ] Illegal termination / retrenchment
    [ ] Workplace harassment (POSH)
    [ ] Maternity benefit denied
    [ ] Something else → free text

Q3. Which state are you in? (affects minimum wage, Shops Act rules)
    [ ] Dropdown of Indian states + UTs

Q4. For how long has this problem been going on?
    [ ] Less than 1 month
    [ ] 1–6 months
    [ ] 6 months – 2 years
    [ ] More than 2 years

Q5. Have you already raised this with HR / your employer?
    [ ] Yes — they refused / ignored
    [ ] Yes — no response for more than 7 days
    [ ] No, not yet

Q6. Approximately how much money is involved? (optional)
    [ ] Up to ₹10,000
    [ ] ₹10,000 – ₹1 lakh
    [ ] More than ₹1 lakh
    [ ] Not sure / not applicable
```

## Wizard Flows

### Wizard 1: Dues Calculator
Calculates gratuity, notice pay, earned leave encashment, and PF shortfall.
Inputs: last drawn salary, years of service, notice period in offer letter, state.

### Wizard 2: POSH Complaint Walkthrough
Step-by-step guide: identify the ICC → file written complaint within 3 months →
what to attach → timeline → what happens next → escalation to Local Complaints
Committee if no ICC exists.

### Wizard 3: Labour Office Complaint
Maps the user's state and issue type to the correct Labour Commissioner office,
generates a complaint letter, explains the conciliation process.
