"""
Vercel entrypoint. Mirrors backend/main.py's API routes but without the
StaticFiles mount — on Vercel, everything in /public is served directly by
the platform, so this function only needs to handle /api/*.

Kept in sync with backend/main.py and its sibling modules, which remain
the canonical source for local development (`uvicorn main:app`) and Docker.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware

from gap_analysis import run_gap_analysis
from keyword_cluster import cluster_keywords
from content_brief import build_brief
from schema_gen import generate_schema
from content_review import review_content

app = FastAPI(title="AI Healthcare Content Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/gap-analysis")
def gap_analysis(site_url: str = Query(...), competitor_url: str = Query(...)):
    try:
        return run_gap_analysis(site_url, competitor_url)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch one of the pages: {e}")
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/keyword-cluster")
def keyword_cluster(payload: dict = Body(...)):
    keywords = payload.get("keywords", "")
    pillar = payload.get("pillar")
    if not keywords.strip():
        raise HTTPException(status_code=400, detail="Provide at least one keyword.")
    return cluster_keywords(keywords, pillar)


@app.post("/api/content-brief")
def content_brief(payload: dict = Body(...)):
    topic = payload.get("topic", "").strip()
    content_type = payload.get("content_type", "disease")
    brand = payload.get("brand", "Your Hospital").strip() or "Your Hospital"
    if not topic:
        raise HTTPException(status_code=400, detail="Provide a topic, e.g. 'Diabetes'.")
    if content_type not in ("disease", "treatment"):
        raise HTTPException(status_code=400, detail="content_type must be 'disease' or 'treatment'.")
    return build_brief(topic, content_type, brand)


@app.post("/api/schema")
def schema(payload: dict = Body(...)):
    schema_type = payload.get("schema_type")
    fields = payload.get("fields", {})
    try:
        return generate_schema(schema_type, fields)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/content-review")
def content_review(payload: dict = Body(...)):
    text = payload.get("text", "")
    if not text.strip():
        raise HTTPException(status_code=400, detail="Paste some content to review.")
    return review_content(text)
