import re
from collections import Counter, defaultdict

from taxonomy import INTENT_KEYWORDS

STOPWORDS = {
    "the", "a", "an", "of", "for", "and", "to", "in", "on", "is", "are",
    "what", "how", "why", "can", "does", "near", "me", "best", "top",
}


def _tokenize(keyword: str) -> list[str]:
    return [w for w in re.findall(r"[a-z]+", keyword.lower()) if w not in STOPWORDS]


def _guess_pillar(keywords: list[str]) -> str:
    counts = Counter()
    for kw in keywords:
        for tok in set(_tokenize(kw)):
            counts[tok] += 1
    if not counts:
        return "General"
    top_word, _ = counts.most_common(1)[0]
    return top_word.title()


def _classify_intent(keyword: str) -> str:
    kw = keyword.lower()
    for intent, triggers in INTENT_KEYWORDS.items():
        for trig in triggers:
            if trig in kw:
                return intent
    return "general"


def cluster_keywords(raw_keywords: str, pillar_hint: str | None = None) -> dict:
    keywords = [k.strip() for k in re.split(r"[,\n]", raw_keywords) if k.strip()]
    keywords = list(dict.fromkeys(keywords))  # de-dupe, preserve order

    pillar = pillar_hint.strip() if pillar_hint and pillar_hint.strip() else _guess_pillar(keywords)

    clusters: dict[str, list[str]] = defaultdict(list)
    for kw in keywords:
        clusters[_classify_intent(kw)].append(kw)

    intent_order = list(INTENT_KEYWORDS.keys()) + ["general"]
    ordered_clusters = [
        {"intent": intent, "keywords": clusters[intent]}
        for intent in intent_order
        if clusters.get(intent)
    ]

    return {
        "pillar": pillar,
        "total_keywords": len(keywords),
        "clusters": ordered_clusters,
        "note": (
            "Clustering is rule-based: each keyword is bucketed by matching "
            "intent phrases (symptom, cause, diagnosis, treatment, diet, doctor, "
            "faq, recovery, complications, cost). The pillar is either the term "
            "you supplied or the most frequent shared word across your keywords."
        ),
    }
