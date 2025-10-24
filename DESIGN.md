
- **Ingestion**
  - Parse PDF per page using pdfminer.six; store (page_text, page_num) chunks
  - Embed chunks with sentence-transformers (`all-MiniLM-L6-v2` by default)
  - Store in FAISS (local) at `storage/vector_index/`
- **Retrieval**
  - Hybrid scoring: semantic kNN + lightweight keyword boost for villa types (3BR/4BR/5BR, Type A/B, “pool”)
  - Post-processing extracts **grounded facts** + **page numbers** for citations
- **Multimodal**
  - `storage/image_map.json`: map villa types to **Rev11** floorplan images (Ground/First)
  - Bootstrapper infers mapping by aligning PDF titles (“3 BEDROOM – TYPE A/B”, “4 BEDROOM TYPE B WITH SWIMMING POOL”, “5 BEDROOM”) with ordered `Rev11-*.webp` pages; can be edited safely
  - On a villa-specific answer, **always** include the appropriate image paths
- **Lead Gen**
  - `lead/detector.py`: regex + heuristics to detect signals (budget, beds, location, timeline, finance/process)
  - `lead/scoring.py`: converts signals + session context to **intent** (low/medium/high) and recommends next action
- **Guardrails**
  - `guardrails.py`: blocks price/availability hallucinations; enforces citations; refuses when confidence < τ
  - PDF over everything else; images are **visual confirmation** only
- **Prompting**
  - `llm/templates/system_chat.txt` provides style: helpful, grounded, subtle urgency; lead-qualification follow-ups

## RAG Strategy

- **Chunking**: page-level (keeps page citations exact)
- **Ranking**: cosine similarity + keyword multipliers for `["3BR","4BR","5BR","Type A","Type B","pool","BUA","plot","balcony"]`
- **Citations**: every property-specific claim lists `{source:"floorplans_pdf", page:<int>}`

## Image Mapping Strategy

- Source of truth: `image_map.json` like:
```json
{
  "3BR-TYPE-A": ["data/WebP/AlBadia_Floorplans_A3_Rev11-1.webp","data/WebP/AlBadia_Floorplans_A3_Rev11-2.webp"],
  "3BR-TYPE-B": ["data/WebP/AlBadia_Floorplans_A3_Rev11-3.webp"],
  "4BR-TYPE-A": ["data/WebP/AlBadia_Floorplans_A3_Rev11-4.webp"],
  "4BR-TYPE-B-POOL": ["data/WebP/AlBadia_Floorplans_A3_Rev11-5.webp","data/WebP/AlBadia_Floorplans_A3_Rev11-7.webp"],
  "5BR": ["data/WebP/AlBadia_Floorplans_A3_Rev11-8.webp","data/WebP/AlBadia_Floorplans_A3_Rev11-9.webp"]
}