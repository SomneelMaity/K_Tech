# S10 MSME & Small Business — Conversation Flow Design

## Intake Flow (≤ 6 questions)

```
Q1. What best describes your business?
    [ ] Sole proprietorship / freelancer
    [ ] Partnership firm
    [ ] Private Limited Company / LLP
    [ ] I am planning to start a business (not yet registered)

Q2. What is the problem you are facing?
    [ ] Client hasn't paid my invoice
    [ ] Cheque bounced
    [ ] Contract dispute / one-sided contract
    [ ] Don't know which licences I need
    [ ] GST / tax filing issue
    [ ] Something else → free text

Q3. Which state are you in? (affects Shops Act, FSSAI state licence, etc.)
    [ ] Dropdown of Indian states + UTs

Q4. Is your business registered as an MSME (Udyam registration)?
    [ ] Yes
    [ ] No, but I qualify (turnover / investment within MSME limits)
    [ ] Not sure

Q5. For the payment issue: how old is the unpaid invoice?
    [ ] Less than 45 days
    [ ] 45 days – 6 months
    [ ] 6 months – 2 years (Samadhaan eligible)
    [ ] More than 2 years
    [ ] Not applicable

Q6. Approximately how much money is owed / at stake?
    [ ] Up to ₹1 lakh
    [ ] ₹1–10 lakh
    [ ] More than ₹10 lakh
    [ ] Not sure / not applicable
```

## Wizard Flows

### Wizard 1: Delayed-Payment Interest Calculator
Inputs: invoice date, payment due date, invoice amount, RBI bank rate on due date.
Formula: compound interest at 3× bank rate from the day after the due date (MSMED §16).
Output: total interest owed + Samadhaan filing guide.

### Wizard 2: Cheque-Bounce Notice (NI Act §138)
Strict 30-day window after bank memo. Generates demand notice with:
- Cheque details (number, date, amount, bank)
- Date of dishonour and reason
- Demand for payment within 15 days
- Warning of criminal prosecution under §138
Alert: deadline countdown shown prominently.

### Wizard 3: Licence Checklist
Inputs: state, business type (food / retail / manufacturing / IT / other), number of employees.
Output: required licences with portal links, approximate fees, and renewal schedule.
(e.g., FSSAI basic/state/central, Shops & Establishments, GST, Professional Tax, Fire NOC)
