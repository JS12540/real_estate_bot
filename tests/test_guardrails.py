from src.rag.guardrails import must_refuse_pricing, enforce_citations

def test_pricing_refusal():
    assert must_refuse_pricing("What's the price?") is True
    assert must_refuse_pricing("availability please") is True
    assert must_refuse_pricing("Tell me BUA") is False

def test_citation_enforcement():
    assert enforce_citations([{"source":"floorplans_pdf","page":5}]) is True
    assert enforce_citations([{"source":"web"}]) is False
