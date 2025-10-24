# Real Estate RAG Chatbot – Al Badia Villas (Dubai Festival City)

An intelligent, **conversion-focused** RAG chatbot that:
- Answers property questions from the **Al Badia Villas** floorplans PDF
- Returns **relevant floorplan images** (Rev11) with each villa discussion
- Detects **buying signals** and **captures lead info**
- **Never** hallucinates prices or availability

> Built per the Candidate Assessment brief. :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

## 1) Quickstart

```bash
# 1) Python env (3.10+ recommended)
uv venv && source .venv/bin/activate     # or: python -m venv .venv

# 2) Install
uv pip install -e .

# 3) Add data
# Place files here (filenames must match):
# data/ABV Final Floorplans.pdf
# data/WebP/AlBadia_Floorplans_A3_Rev11-1.webp ... -9.webp

# 4) Environment
cp .env.example .env
# Fill in OPENAI_API_KEY (or set PROVIDER=local to use a local model via Transformers)

# 5) Build vector index + image map
python scripts/build_index.py
python scripts/bootstrap_image_map.py   # creates/updates storage/image_map.json

# 6) Run API
uvicorn src.app.main:app --reload
