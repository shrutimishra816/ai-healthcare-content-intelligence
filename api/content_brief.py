from taxonomy import (
    FAQ_TEMPLATES_DISEASE, FAQ_TEMPLATES_TREATMENT,
    HEADING_SKELETON_DISEASE, HEADING_SKELETON_TREATMENT, EEAT_CHECKLIST,
)
from schema_gen import generate_schema


def build_brief(topic: str, content_type: str, brand: str = "Your Hospital") -> dict:
    topic = topic.strip()
    is_disease = content_type == "disease"

    faq_templates = FAQ_TEMPLATES_DISEASE if is_disease else FAQ_TEMPLATES_TREATMENT
    faqs = [t.format(topic=topic) for t in faq_templates]

    headings = HEADING_SKELETON_DISEASE if is_disease else HEADING_SKELETON_TREATMENT

    title = f"{topic}: {'Symptoms, Causes & Treatment' if is_disease else 'Procedure, Recovery & Cost'} | {brand}"
    meta_description = (
        f"Learn about {topic.lower()} — {'symptoms, causes, diagnosis and treatment options' if is_disease else 'how it works, recovery time, risks and cost'} "
        f"explained by specialists at {brand}. Book a consultation today."
    )

    internal_links = (
        [f"Related condition pages", f"Doctors treating {topic}", "Book an appointment page", "Insurance/cost page"]
        if is_disease
        else [f"Conditions {topic} treats", f"Surgeons performing {topic}", "Book an appointment page", "Cost & insurance page"]
    )

    schema_type = "MedicalCondition" if is_disease else "MedicalTherapy"
    schema_fields = (
        {"name": topic, "description": meta_description, "treatments": "", "symptoms": ""}
        if is_disease
        else {"name": topic, "description": meta_description}
    )
    condition_schema = generate_schema(schema_type, schema_fields)
    faq_schema = generate_schema(
        "FAQPage",
        {"qa_pairs": [{"question": q, "answer": "[Write a concise, medically-reviewed answer here]"} for q in faqs]},
    )

    geo_checklist = [
        f"Does the page answer 'What is {topic}?' in the first 2 sentences, in plain language an AI could quote directly?",
        "Is there a dedicated FAQ section with FAQPage schema markup?",
        "Are symptoms/steps/options presented as scannable lists, not just paragraphs?",
        "Is there a named, credentialed medical reviewer and a visible last-updated date?",
        "Does the page link to at least one authoritative external source (WHO, NIH, ICMR, PubMed)?",
    ]

    return {
        "topic": topic,
        "content_type": content_type,
        "title": title,
        "meta_description": meta_description,
        "heading_structure": headings,
        "faqs": faqs,
        "internal_link_suggestions": internal_links,
        "external_reference_guidance": (
            "Cite at least one peer-reviewed or health-authority source per major claim "
            "(e.g. WHO, NIH, ICMR, PubMed). This tool does not fetch live citations — "
            "add the specific source URLs during writing/medical review."
        ),
        "eeat_checklist": EEAT_CHECKLIST,
        "geo_readiness_checklist": geo_checklist,
        "schema": {"primary": condition_schema, "faq": faq_schema},
    }
