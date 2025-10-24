from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from sentence_transformers import SentenceTransformer
import numpy as np, faiss, os, orjson
from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger("ingest")

def load_pdf_pages(pdf_path: str):
    pages = []
    for i, page_layout in enumerate(extract_pages(pdf_path)):
        texts = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                texts.append(element.get_text())
        page_text = "\n".join(texts).strip()
        if page_text:
            pages.append({"page": i+1, "text": page_text})
    return pages

def build_index(pages):
    model = SentenceTransformer(settings.EMBEDDING_MODEL)
    embeddings = model.encode([p["text"] for p in pages], convert_to_numpy=True, normalize_embeddings=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    meta = {"pages": pages}
    os.makedirs(settings.INDEX_DIR, exist_ok=True)
    faiss.write_index(index, os.path.join(settings.INDEX_DIR, "faiss.index"))
    with open(os.path.join(settings.INDEX_DIR, "meta.json"), "wb") as f:
        f.write(orjson.dumps(meta))
    logger.info(f"Indexed {len(pages)} pages -> {settings.INDEX_DIR}")

def run():
    pages = load_pdf_pages(settings.PDF_PATH)
    build_index(pages)

if __name__ == "__main__":
    run()
