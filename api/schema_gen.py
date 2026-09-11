def generate_schema(schema_type: str, fields: dict) -> dict:
    """Builds valid, ready-to-use schema.org JSON-LD from user-supplied fields."""
    generators = {
        "MedicalCondition": _medical_condition,
        "MedicalTherapy": _medical_therapy,
        "MedicalOrganization": _medical_organization,
        "Physician": _physician,
        "FAQPage": _faq_page,
        "LocalBusiness": _local_business,
        "BreadcrumbList": _breadcrumb_list,
    }
    if schema_type not in generators:
        raise ValueError(f"Unknown schema type: {schema_type}")
    return generators[schema_type](fields)


def _medical_condition(f):
    return {
        "@context": "https://schema.org",
        "@type": "MedicalCondition",
        "name": f.get("name", ""),
        "description": f.get("description", ""),
        "possibleTreatment": [
            {"@type": "MedicalTherapy", "name": t.strip()}
            for t in f.get("treatments", "").split(",") if t.strip()
        ],
        "signOrSymptom": [
            {"@type": "MedicalSignOrSymptom", "name": s.strip()}
            for s in f.get("symptoms", "").split(",") if s.strip()
        ],
    }


def _medical_therapy(f):
    return {
        "@context": "https://schema.org",
        "@type": "MedicalTherapy",
        "name": f.get("name", ""),
        "description": f.get("description", ""),
    }


def _medical_organization(f):
    return {
        "@context": "https://schema.org",
        "@type": "MedicalOrganization",
        "name": f.get("name", ""),
        "url": f.get("url", ""),
        "telephone": f.get("phone", ""),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": f.get("street", ""),
            "addressLocality": f.get("city", ""),
            "addressRegion": f.get("region", ""),
            "postalCode": f.get("postal_code", ""),
            "addressCountry": f.get("country", ""),
        },
        "medicalSpecialty": [s.strip() for s in f.get("specialties", "").split(",") if s.strip()],
    }


def _physician(f):
    return {
        "@context": "https://schema.org",
        "@type": "Physician",
        "name": f.get("name", ""),
        "medicalSpecialty": [s.strip() for s in f.get("specialties", "").split(",") if s.strip()],
        "url": f.get("url", ""),
        "worksFor": {"@type": "MedicalOrganization", "name": f.get("hospital", "")},
    }


def _faq_page(f):
    qas = f.get("qa_pairs", [])
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": qa.get("question", ""),
                "acceptedAnswer": {"@type": "Answer", "text": qa.get("answer", "")},
            }
            for qa in qas
            if qa.get("question")
        ],
    }


def _local_business(f):
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": f.get("name", ""),
        "url": f.get("url", ""),
        "telephone": f.get("phone", ""),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": f.get("street", ""),
            "addressLocality": f.get("city", ""),
            "addressRegion": f.get("region", ""),
            "postalCode": f.get("postal_code", ""),
            "addressCountry": f.get("country", ""),
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": f.get("latitude", ""),
            "longitude": f.get("longitude", ""),
        } if f.get("latitude") else None,
    }


def _breadcrumb_list(f):
    items = f.get("items", [])
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item.get("name", ""),
                "item": item.get("url", ""),
            }
            for i, item in enumerate(items)
        ],
    }
