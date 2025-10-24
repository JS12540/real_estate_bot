import os, orjson, numpy as np, faiss, regex as re
from sentence_transformers import SentenceTransformer
from src.core.config import settings

KEYBOOST = [
    ("3 BR", 0.05), ("4 BR", 0.08), ("5 BR", 0.1),
    ("3 BEDROOM", 0.05), ("4 BEDROOM", 0.08), ("5 BEDROOM", 0.1),
    ("TYPE A", 0.05), ("TYPE B", 0.05),
    ("POOL", 0.06), ("BUA", 0.06), ("PLOT", 0.06), ("BALCONY", 0.03)
]

class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.index = faiss.read_index(os.path.join(settings.INDEX_DIR, "faiss.index"))
        with open(os.path.join(settings.INDEX_DIR, "meta.json"), "rb") as f:
            self.meta = orjson.loads(f.read())

    def _keyword_bonus(self, text: str, query: str) -> float:
        t = (text + " " + query).upper()
        return sum(w for k, w in KEYBOOST if k in t)

    def search(self, query: str, k: int = 4):
        qv = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        sims, idxs = self.index.search(qv, k)
        results = []
        for rank, (score, idx) in enumerate(zip(sims[0], idxs[0])):
            page = self.meta["pages"][idx]
            bonus = self._keyword_bonus(page["text"], query)
            results.append({
                "rank": rank,
                "score": float(score + bonus),
                "page": page["page"],
                "text": page["text"]
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

def extract_villa_types(text: str):
    # Returns normalized tags like "3BR-TYPE-A", "4BR-TYPE-B-POOL", "5BR"
    t = text.upper()
    br = None
    if re.search(r"\b5\s*BEDROOM|\b5\s*BR", t): br = "5BR"
    elif re.search(r"\b4\s*BEDROOM|\b4\s*BR", t): br = "4BR"
    elif re.search(r"\b3\s*BEDROOM|\b3\s*BR", t): br = "3BR"

    typ = None
    if re.search(r"TYPE\s*A\b", t): typ = "TYPE-A"
    elif re.search(r"TYPE\s*B\b", t): typ = "TYPE-B"

    pool = "-POOL" if "POOL" in t or "SWIMMING POOL" in t else ""
    if br and typ:
        return [f"{br}-{typ}{pool}"]
    if br:
        return [br]
    return []
