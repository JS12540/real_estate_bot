def score(signals: list, context: dict):
    weights = {
        "contact_info_shared": 3.0,
        "budget_mention": 2.0,
        "timeline": 2.0,
        "specific_requirements": 1.5,
        "location_preference": 1.0,
        "comparison": 1.0,
        "financing_question": 1.5,
    }
    s = sum(weights.get(sig, 1.0) for sig in signals)
    if s >= 6: intent = "high"
    elif s >= 3: intent = "medium"
    else: intent = "low"

    if "contact_info_shared" in signals:
        reco = "offer_viewing"
    elif "specific_requirements" in signals:
        reco = "show_floorplans_and_qualify"
    else:
        reco = "ask_preferences"
    return {"intent": intent, "recommended_action": reco}
