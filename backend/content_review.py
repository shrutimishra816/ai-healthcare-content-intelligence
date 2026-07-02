import re

from taxonomy import ALL_TOPICS

VOWELS = "aeiouy"


def _count_syllables(word: str) -> int:
    word = word.lower()
    word = re.sub(r"[^a-z]", "", word)
    if not word:
        return 0
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def _flesch_reading_ease(text: str) -> float:
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    words = re.findall(r"[A-Za-z']+", text)
    if not sentences or not words:
        return 0.0
    syllables = sum(_count_syllables(w) for w in words)
    n_sentences, n_words = len(sentences), len(words)
    score = 206.835 - 1.015 * (n_words / n_sentences) - 84.6 * (syllables / n_words)
    return round(max(0.0, min(100.0, score)), 1)


def _readability_label(score: float) -> str:
    if score >= 70:
        return "easy — accessible to a general patient audience"
    if score >= 50:
        return "moderate — some medical/technical phrasing"
    return "difficult — dense or highly technical phrasing"


def review_content(text: str) -> dict:
    text = text.strip()
    words = re.findall(r"[A-Za-z']+", text)
    word_count = len(words)

    flesch = _flesch_reading_ease(text)

    lower = text.lower()
    entities_found = sorted({t for t in ALL_TOPICS if re.search(r"\b" + re.escape(t.lower()) + r"\b", lower)})
    entity_coverage_score = min(100, len(entities_found) * 12)

    # Heuristic, pattern-based trust / E-E-A-T signal detection.
    has_reviewer = bool(re.search(r"reviewed by|medically reviewed|dr\.\s?\w+.*\b(md|do|mbbs)\b", lower))
    has_date = bool(re.search(r"\b(20\d{2})\b", text)) and bool(
        re.search(r"updated|reviewed|published", lower)
    )
    has_citation_language = bool(re.search(r"according to|study (found|shows)|research (shows|indicates)|source:", lower))
    has_disclaimer = bool(re.search(r"not (a substitute|intended as) .*(medical advice|diagnosis)|consult (a|your) doctor", lower))

    trust_signals = {
        "medical_reviewer_mentioned": has_reviewer,
        "date_signal_present": has_date,
        "citation_language_present": has_citation_language,
        "medical_disclaimer_present": has_disclaimer,
    }
    trust_score = round(100 * sum(trust_signals.values()) / len(trust_signals))

    overall = round((entity_coverage_score * 0.4) + (trust_score * 0.35) + (min(100, flesch) * 0.25))

    recs = []
    if not has_reviewer:
        recs.append("Add a named medical reviewer with credentials (e.g. 'Reviewed by Dr. X, MBBS, MD').")
    if not has_date:
        recs.append("Add a visible 'last updated' or 'last reviewed' date.")
    if not has_citation_language:
        recs.append("Reference at least one study or health authority explicitly in the text.")
    if not has_disclaimer:
        recs.append("Add a medical disclaimer directing readers to consult a doctor.")
    if flesch < 50:
        recs.append("Simplify sentence structure — current reading level is dense for a patient audience.")
    if entity_coverage_score < 40:
        recs.append("Mention more specific, recognizable medical terms (symptoms, treatments, tests) so AI engines can match this page to real queries.")
    if not recs:
        recs.append("Strong foundation across trust and readability signals — focus next on expanding depth and citations.")

    return {
        "word_count": word_count,
        "readability": {
            "flesch_reading_ease": flesch,
            "label": _readability_label(flesch),
        },
        "entity_coverage": {
            "score": entity_coverage_score,
            "entities_found": entities_found,
        },
        "trust_signals": trust_signals,
        "scores": {
            "trust_score": trust_score,
            "entity_coverage_score": entity_coverage_score,
            "overall_content_score": overall,
        },
        "recommendations": recs,
        "note": (
            "Readability (Flesch Reading Ease) and entity coverage are computed directly "
            "from your text. Trust/E-E-A-T signals are detected via pattern matching "
            "(phrases like 'reviewed by Dr.', dated language, citation phrasing, disclaimers) "
            "as a heuristic proxy — not a live medical-accuracy or legal review."
        ),
    }
