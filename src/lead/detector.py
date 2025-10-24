import regex as re

PATTERNS = {
    "budget_mention": r"(?i)\bAED\s?\d|budget|price range|under\s?\d",
    "specific_requirements": r"(?i)\b(3|4|5)\s*bed(room)?s?\b|type\s*[ab]\b|pool|plot|bua",
    "location_preference": r"(?i)festival city|dubai|al badia",
    "timeline": r"(?i)move|moving|timeline|by (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)|within \d+ (days|weeks|months)",
    "comparison": r"(?i)compare|difference|vs\.?|versus",
    "financing_question": r"(?i)mortgage|finance|payment|installment|down payment|documentation|title",
    "contact_info_shared": r"(?i)\b\d{7,}\b|@\w+\.\w+"
}

def detect_signals(text: str):
    hits = [k for k,pat in PATTERNS.items() if re.search(pat, text)]
    return hits
