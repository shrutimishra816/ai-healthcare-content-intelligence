import re

import requests
from bs4 import BeautifulSoup

from taxonomy import DISEASES, TREATMENTS, DEPARTMENTS

USER_AGENT = "Mozilla/5.0 (compatible; ContentIntelBot/1.0)"


def fetch_text(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=12)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    parts = [soup.get_text(" ", strip=True)]
    if soup.title:
        parts.append(soup.title.get_text(strip=True))
    for h in soup.find_all(re.compile("^h[1-3]$")):
        parts.append(h.get_text(" ", strip=True))
    return " ".join(parts).lower()


def topics_present(text: str, topics: list[str]) -> set[str]:
    found = set()
    for topic in topics:
        pattern = r"\b" + re.escape(topic.lower()) + r"\b"
        if re.search(pattern, text):
            found.add(topic)
    return found


def run_gap_analysis(site_url: str, competitor_url: str) -> dict:
    site_text = fetch_text(site_url)
    comp_text = fetch_text(competitor_url)

    site_diseases = topics_present(site_text, DISEASES)
    comp_diseases = topics_present(comp_text, DISEASES)
    site_treatments = topics_present(site_text, TREATMENTS)
    comp_treatments = topics_present(comp_text, TREATMENTS)
    site_departments = topics_present(site_text, DEPARTMENTS)
    comp_departments = topics_present(comp_text, DEPARTMENTS)

    missing_diseases = sorted(comp_diseases - site_diseases)
    missing_treatments = sorted(comp_treatments - site_treatments)
    missing_departments = sorted(comp_departments - site_departments)

    total_comp_topics = len(comp_diseases) + len(comp_treatments) + len(comp_departments)
    total_missing = len(missing_diseases) + len(missing_treatments) + len(missing_departments)
    coverage_pct = (
        round(100 * (1 - total_missing / total_comp_topics)) if total_comp_topics else 100
    )

    return {
        "site_url": site_url,
        "competitor_url": competitor_url,
        "coverage_vs_competitor_pct": max(0, coverage_pct),
        "site_topics_found": {
            "diseases": sorted(site_diseases),
            "treatments": sorted(site_treatments),
            "departments": sorted(site_departments),
        },
        "competitor_topics_found": {
            "diseases": sorted(comp_diseases),
            "treatments": sorted(comp_treatments),
            "departments": sorted(comp_departments),
        },
        "missing_on_site": {
            "diseases": missing_diseases,
            "treatments": missing_treatments,
            "departments": missing_departments,
        },
        "note": (
            "Coverage is checked against a curated taxonomy of common hospital-website "
            "topics by scanning each page's visible text and headings. It reflects "
            "whether a topic is mentioned on the page you gave us, not full page "
            "quality or depth of coverage."
        ),
    }
