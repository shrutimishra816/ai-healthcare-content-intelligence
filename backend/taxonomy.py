"""
A curated taxonomy of common hospital-website topics. This is the reference
set the Content Gap Analyzer checks pages against, and the entity list the
Content Reviewer uses for entity-coverage scoring.

Extend these lists for other specialties/markets — they're deliberately
kept to well-known, unambiguous terms so gap detection stays accurate.
"""

DISEASES = [
    "Diabetes", "Thyroid", "PCOS", "PCOD", "Hypertension", "Asthma",
    "Arthritis", "Osteoporosis", "Cataract", "Glaucoma", "Kidney Stones",
    "Chronic Kidney Disease", "Fatty Liver", "Hepatitis", "Migraine",
    "Epilepsy", "Anemia", "Obesity", "Infertility", "Endometriosis",
    "Fibroids", "Hernia", "Piles", "Fissure", "Gallstones", "Appendicitis",
    "Coronary Artery Disease", "Heart Failure", "Stroke", "Varicose Veins",
    "Psoriasis", "Eczema", "Vitiligo", "Sleep Apnea", "Sinusitis",
    "Tonsillitis", "Cervical Spondylosis", "Slip Disc", "Scoliosis",
]

TREATMENTS = [
    "IVF", "IUI", "Knee Replacement", "Hip Replacement", "Cataract Surgery",
    "LASIK", "Angioplasty", "Bypass Surgery", "Dialysis", "Kidney Transplant",
    "Liver Transplant", "Chemotherapy", "Radiation Therapy", "Physiotherapy",
    "Root Canal", "Dental Implants", "Bariatric Surgery", "Laparoscopy",
    "Endoscopy", "Colonoscopy", "Spine Surgery", "ACL Reconstruction",
    "C-Section", "Normal Delivery", "Hysterectomy", "Thyroidectomy",
    "Gallbladder Surgery", "Hernia Surgery", "Piles Surgery",
    "Cochlear Implant", "Pacemaker Implant", "Stent Placement",
]

DEPARTMENTS = [
    "Cardiology", "Orthopedics", "Gynecology", "Neurology", "Oncology",
    "Nephrology", "Urology", "Gastroenterology", "Pulmonology",
    "Endocrinology", "Dermatology", "ENT", "Ophthalmology", "Pediatrics",
    "Psychiatry", "Dentistry", "General Surgery", "Emergency Medicine",
]

ALL_TOPICS = DISEASES + TREATMENTS

INTENT_KEYWORDS = {
    "symptoms": ["symptom", "sign", "signs", "warning"],
    "causes": ["cause", "reason", "why"],
    "diagnosis": ["diagnos", "test", "detect", "scan"],
    "treatment": ["treatment", "cure", "therapy", "surgery", "medicine", "procedure"],
    "diet": ["diet", "food", "nutrition", "eat"],
    "doctor": ["doctor", "specialist", "physician", "surgeon"],
    "faq": ["what is", "what are", "how", "can", "does", "is it"],
    "recovery": ["recovery", "recover", "heal", "after"],
    "complications": ["complication", "risk", "side effect", "danger"],
    "cost": ["cost", "price", "charges", "insurance"],
}

FAQ_TEMPLATES_DISEASE = [
    "What is {topic}?",
    "What are the early symptoms of {topic}?",
    "What causes {topic}?",
    "How is {topic} diagnosed?",
    "What are the treatment options for {topic}?",
    "Is {topic} curable?",
    "Who is at risk of {topic}?",
    "How can {topic} be prevented?",
    "When should I see a doctor about {topic}?",
]

FAQ_TEMPLATES_TREATMENT = [
    "What is {topic}?",
    "Who needs {topic}?",
    "How is {topic} performed?",
    "What is the recovery time after {topic}?",
    "What are the risks of {topic}?",
    "How much does {topic} cost?",
    "What is the success rate of {topic}?",
    "How should I prepare for {topic}?",
]

HEADING_SKELETON_DISEASE = [
    "Overview", "Symptoms", "Causes & Risk Factors", "Diagnosis",
    "Treatment Options", "Prevention", "Frequently Asked Questions",
    "When to See a Doctor",
]

HEADING_SKELETON_TREATMENT = [
    "Overview", "Who Needs This Procedure", "How It's Performed",
    "Preparation", "Recovery & Aftercare", "Risks & Complications",
    "Cost", "Frequently Asked Questions",
]

EEAT_CHECKLIST = [
    "Byline with author name and credentials",
    "Medical reviewer name and credentials (e.g. 'Reviewed by Dr. X, MD')",
    "Visible 'last updated' or 'last reviewed' date",
    "At least one citation to a peer-reviewed source or health authority (e.g. WHO, NIH, ICMR)",
    "Clear medical disclaimer",
    "Link to the reviewing doctor's or hospital's profile page",
]
