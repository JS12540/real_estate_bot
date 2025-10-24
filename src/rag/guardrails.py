from typing import List

FORBIDDEN = ["PRICE", "PRICING", "COST", "AVAILABILITY", "AVAILABLE", "DISCOUNT", "OFFER"]

def must_refuse_pricing(user_msg: str) -> bool:
    t = user_msg.upper()
    return any(w in t for w in FORBIDDEN)

def enforce_citations(citations: List[dict]) -> bool:
    # require at least one floorplans_pdf citation with page
    return any(c.get("source") == "floorplans_pdf" and isinstance(c.get("page"), int) for c in citations)
