# AI-Assisted B2B Lead Qualification Framework
### Using LLM + ICP (Ideal Customer Profile) as an Automated Lead Scoring Sieve


## Overview

An AI-assisted workflow for qualifying scraped B2B prospects using ICP (Ideal Customer Profile) signals, structured scoring logic, and LLM-based classification.

Instead of generating cold emails directly from noisy crawl data, this framework introduces a qualification layer first:

- Tag prospects
- Score ICP fit
- Filter low-quality leads
- Output structured qualification results

Designed for scalable outbound prospecting workflows.


## Future Improvements

- Embedding-based ICP similarity search
- Streamlit review dashboard
- CRM integration
- Human-in-the-loop validation
- Batch async processing
- Multi-ICP weighting system
- Vector database retrieval

---

## Background & Motivation

In B2B outbound sales, one of the most overlooked costs is **the time spent manually evaluating whether a prospect is worth pursuing at all**.

After years in hardware OEM/ODM manufacturing, I noticed a recurring pattern: experienced salespeople carry an implicit mental model of what a "good fit" customer looks like — built from years of successful deals. But that model lives in their heads, not in any system.

This project externalizes that mental model into a structured **ICP (Ideal Customer Profile)** dataset, then uses an LLM to apply it automatically against large batches of scraped prospect data.

The goal is not to replace human judgment. It is to eliminate the 80% of names that clearly don't fit — before any human time is spent on them.

---

## The Core Problem This Solves

Imagine you scrape 500 company websites from a trade directory. You now have:
- Company names
- Website URLs
- About Us text
- Product descriptions

The question is: **which of these 500 are worth a cold outreach?**

Without a system, you read each one manually. With this framework, you define your ICP once — based on customers you've already successfully worked with — and let the LLM score and label each prospect automatically.

---

## Architecture: Three Layers

```
┌─────────────────────────────────────────────────────┐
│  Layer 1: ICP Knowledge Base                        │
│  (Who is our ideal customer? What signals matter?)  │
│  → sample_icp.csv                                   │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  Layer 2: Lead Qualifier (LLM-powered)              │
│  (Does this scraped prospect match any ICP profile?)│
│  → qualifier.py + prompts/lead_qualifier.txt        │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  Layer 3: Scored & Labeled Output                   │
│  (Pass/Fail, ICP label, confidence, reason)         │
│  → output/scored_leads.csv                          │
└─────────────────────────────────────────────────────┘
```

**Layer 1 and Layer 2 are intentionally separated.**

The ICP data defines *what to look for*. The qualifier script defines *how to look*. This separation means you can update your ICP profiles without touching the code, and vice versa.

---

## What This Project Is (and Is Not)

**This is a framework and architecture demonstration.**

The sample data in this repository is synthetic — constructed to reflect realistic B2B scenarios in the specialty lighting / optical components industry, without exposing any real client information.

The underlying business logic (ICP structure, scoring criteria, prompt design) is derived from real experience in hardware OEM/ODM sales development, but all company names and specific data points are fictional.

---

## Repository Structure

```
b2b-lead-qualification-framework/
├── README.md                    ← You are here
├── data/
│   ├── sample_icp.csv           ← ICP profiles (synthetic)
│   └── sample_prospects.csv     ← Scraped prospect data (synthetic)
├── prompts/
│   └── lead_qualifier.txt       ← LLM prompt template
├── scripts/
│   └── qualifier.py             ← Main qualification script
├── output/
│   └── scored_leads.csv         ← Example output (pre-generated)
└── docs/
    └── icp_field_design.md      ← Field design rationale
```


## Installation

```bash
git clone https://github.com/yourname/b2b-lead-qualification-framework.git

cd b2b-lead-qualification-framework

pip install -r requirements.txt
```

---

## How It Works

### Step 1 — Define your ICP profiles (`data/sample_icp.csv`)

Each row represents one type of ideal customer, defined by:
- **Target Label** — internal category name
- **Value Chain Position** — where they sit in the industry (Manufacturer, Designer, Distributor)
- **Market Vertical** — end application (e.g., Architectural Lighting, Museum Display, Sauna & Spa)
- **Positive Signals** — keywords that indicate a good fit
- **Negative Signals** — keywords that disqualify a prospect immediately
- **Reference Companies** — 1-2 fictional examples of what this profile looks like

### Step 2 — Load your scraped prospects (`data/sample_prospects.csv`)

Each row is one company with whatever raw data you were able to scrape: URL, About Us text, product descriptions, LinkedIn summary, etc.

### Step 3 — Run the qualifier

```bash
pip install anthropic pandas
export ANTHROPIC_API_KEY=your_key_here
python scripts/qualifier.py
```

### Step 4 — Review the scored output (`output/scored_leads.csv`)

Each prospect gets:

| Field | Example |
|---|---|
| `match` | `PASS` / `FAIL` / `UNCERTAIN` |
| `icp_label` | `Specialty OEM - Fast Sampling` |
| `confidence` | `87%` |
| `reason` | `Website mentions IP68 custom luminaires and short prototype cycles` |


## Example Output

| company | fit_score | fit_status | customer_type | confidence |
|---|---|---|---|---|
| Alpha Lighting | 84 | PASS | Lighting Manufacturer | High |
| Beta Retail | 21 | FAIL | Consumer Retailer | High |
| Gamma Studio | 68 | UNCERTAIN | Lighting Consultant | Medium |

Example reasoning:

```json
{
  "positive_signals": [
    "custom luminaires",
    "architectural lighting",
    "LED systems"
  ],
  "negative_signals": [],
  "confidence": "High"
}
```

---

## Prompt Design Philosophy

The LLM prompt is structured around three constraints:

1. **Anchor to ICP, not to assumptions** — The model is explicitly told to score only against the provided ICP profiles, not to infer or invent new categories.
2. **Require evidence** — Every label must be justified by specific text found in the prospect's data. If no evidence exists, output `UNCERTAIN`, not a guess.
3. **Hard output format** — JSON only. No prose. This makes downstream processing reliable.

See `prompts/lead_qualifier.txt` for the full template.


## Why Separate Qualification from Email Generation?

Most AI outbound systems attempt to generate personalized emails immediately after scraping prospect data.

This framework intentionally separates:

1. Prospect Qualification
2. Pain Analysis
3. Email Generation

Why?

Because inaccurate or low-confidence crawl data often causes LLMs to hallucinate detailed assumptions about the prospect.

By inserting a qualification layer first, the workflow becomes:

- More scalable
- More explainable
- Easier to audit
- Less prone to hallucination
- More operationally useful for real B2B sales teams

---

## Why This Approach

Most outbound automation tools jump straight to personalized email generation. The problem is: personalization requires knowing *who you're talking to*. If you haven't validated the prospect first, you end up generating elaborate, well-written emails to the wrong companies.

This framework inserts a qualification gate before any outreach content is created. It is deliberately minimal — the output is a label and a reason, nothing more. The email generation layer is a separate concern.

---

## Tech Stack

- Python
- Pandas
- Claude API / LLM integration
- Structured prompt engineering
- CSV-based data pipeline
- ICP scoring architecture
- AI-assisted lead qualification workflow

---

## Background

This project is built from practical experience in OEM/ODM hardware manufacturing and outbound B2B sales workflows. The framework reflects a real operational bottleneck rather than a tutorial-style exercise.

---

## License

MIT
