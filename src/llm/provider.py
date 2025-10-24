from typing import Dict
from src.core.config import settings

def chat_complete(system: str, user: str) -> str:
    """
    Very small abstraction that supports OpenAI or a 'local' echo-style fallback.
    For real use, plug in your preferred model/provider here.
    """
    if settings.PROVIDER == "local":
        # minimal local stub: return a short, polite echo (retrieval does the factual heavy lifting)
        return f"{user.strip()}"

    # OpenAI example
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=0.2,
    )
    return resp.choices[0].message.content
