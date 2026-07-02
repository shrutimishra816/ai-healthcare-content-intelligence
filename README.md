# AI Healthcare Content Intelligence Platform

From keyword research to AI-ready healthcare content in minutes. Five real,
working modules for planning and QA-ing hospital website content:

1. **Content Gap Analysis** — fetches your page and a competitor's page live,
   and diffs topic coverage (diseases, treatments, departments) against a
   curated healthcare taxonomy.
2. **Keyword Clustering** — groups raw keyword lists into a pillar/intent
   structure (symptoms, causes, diagnosis, treatment, diet, doctor, FAQ,
   recovery, complications, cost) using rule-based intent matching.
3. **AI Content Brief Generator** — produces a title, meta description,
   heading skeleton, FAQ list, internal-link plan, E-E-A-T checklist, GEO
   readiness checklist, and ready-to-paste schema.org JSON-LD for a topic.
4. **Schema Generator** — a standalone tool for generating valid JSON-LD
   (MedicalCondition, MedicalTherapy, MedicalOrganization, Physician,
   FAQPage, LocalBusiness, BreadcrumbList).
5. **Content Review** — paste a draft, get a real Flesch Reading Ease score,
   entity-coverage score, and heuristic trust/E-E-A-T signal detection
   (medical reviewer, date, citations, disclaimer).

## What's real vs. estimated

Everything is computed directly from what you give it — no mocked data.
Readability, entity coverage, gap analysis, clustering, and schema output
are deterministic, inspectable code (see `backend/`). The **trust/E-E-A-T
signals** in Content Review and the **GEO readiness checklist** in the
brief generator are explicitly labeled **heuristics**: pattern-matching
proxies for genuine editorial/medical review, not a substitute for one.
This tool does not call any LLM API — every module runs on rule-based
logic, which also means it's free to self-host with no API keys required.

## Run it locally

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Open **http://localhost:8000**.

## Run it with Docker

```bash
docker build -t ai-healthcare-content-intelligence .
docker run -p 8000:8000 ai-healthcare-content-intelligence
```

## Tech stack

- **Backend:** FastAPI, BeautifulSoup, requests
- **Frontend:** vanilla HTML/CSS/JS, no build step, served as static files
  by FastAPI
- **Taxonomy:** `backend/taxonomy.py` — extend the disease/treatment/
  department lists for other specialties or markets

## Part of the Growth OS suite

Pairs with the **AI Visibility Intelligence Platform** (SEO/AEO/GEO page
scoring) as modules of a single healthcare growth platform.
