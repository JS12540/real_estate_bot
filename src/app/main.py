from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from src.core.prompts import SYSTEM_PROMPT, REFUSAL_PRICING
from src.llm.provider import chat_complete
from src.rag.retriever import Retriever, extract_villa_types
from src.rag.postprocess import extract_specs
from src.rag.guardrails import must_refuse_pricing, enforce_citations
from src.images.mapping import load_image_map, find_images_for
from src.lead.detector import detect_signals
from src.lead.scoring import score

app = FastAPI(title="Real Estate RAG Chatbot")

retriever = Retriever()
image_map = load_image_map()

class ChatRequest(BaseModel):
    message: str
    session_id: str
    context: Dict[str, Any] = Field(default_factory=dict)

class ChatResponse(BaseModel):
    response: str
    properties_mentioned: List[str]
    citations: List[Dict[str, Any]]
    images: List[Dict[str, Any]]
    lead_signals: Dict[str, Any]
    follow_up_prompt: str

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    user_msg = req.message.strip()

    # Guardrail on pricing/availability
    pricing_refusal = must_refuse_pricing(user_msg)

    # Retrieve top pages
    hits = retriever.search(user_msg, k=4)

    # Compose grounded text + citations
    top = hits[0] if hits else None
    grounded_facts = top["text"][:1800] if top else ""
    citations = []
    if top:
        citations.append({"source":"floorplans_pdf", "page": top["page"]})

    # Extract villa tags & specs
    tags = []
    for h in hits:
        tags += extract_villa_types(h["text"])
    tags = list(dict.fromkeys(tags))  # unique, preserve order

    specs = extract_specs(grounded_facts)
    imgs = find_images_for(tags, image_map)

    # Property labels
    properties_mentioned = tags

    # Ensure we always cite the PDF for property details
    if not enforce_citations(citations):
        # If we somehow couldn't cite, be conservative
        return ChatResponse(
            response="I couldn’t verify property details confidently from the floorplans PDF. I can connect you with an agent for accurate information.",
            properties_mentioned=[],
            citations=[],
            images=[],
            lead_signals={"intent":"low","signals_detected":[],"recommended_action":"ask_preferences"},
            follow_up_prompt="Could you share if you’re looking for 3, 4, or 5 bedrooms and your move-in timeline?"
        )

    # Build answer to feed to the LLM (LLM provides tone; facts & images already grounded)
    fact_block = []
    if "bua_sqm" in specs: fact_block.append(f"Total BUA: {specs['bua_sqm']} SQM.")
    if "plot_sqm_range" in specs: fact_block.append(f"Plot size range: {specs['plot_sqm_range'][0]}–{specs['plot_sqm_range'][1]} SQM.")

    fact_text = " ".join(fact_block) if fact_block else "See cited floorplan page for specifications."

    # Lead detection
    signals = detect_signals(user_msg)
    lead = score(signals, req.context)

    # Build user-visible message
    if pricing_refusal:
        assistant_text = REFUSAL_PRICING + " " + "Based on the floorplans, " + fact_text
    else:
        assistant_text = "Based on the Al Badia Villas floorplans, " + fact_text

    # Friendly follow-up for conversion
    follow_up = "I can send you detailed floor plans and arrange a site visit. What’s your preferred timeline for moving, and may I have your name, email, and phone to coordinate?"

    # Final LLM polish (kept minimal temp; core facts already fixed)
    final_text = chat_complete(SYSTEM_PROMPT, assistant_text)

    return ChatResponse(
        response=final_text,
        properties_mentioned=properties_mentioned,
        citations=citations,
        images=imgs,
        lead_signals={"intent": lead["intent"], "signals_detected": signals, "recommended_action": lead["recommended_action"]},
        follow_up_prompt=follow_up
    )
