import os, json, regex as re
from src.core.config import settings
from src.rag.ingest import load_pdf_pages

"""
Creates/updates storage/image_map.json by heuristically aligning PDF headings with
ordered Rev11 images. You can edit the JSON later for exact control.
"""

HEADINGS = [
    ("3BR-TYPE-A", r"(?i)\b3\s*BEDROOM\b.*TYPE\s*A"),
    ("3BR-TYPE-B", r"(?i)\b3\s*BEDROOM\b.*TYPE\s*B"),
    ("4BR-TYPE-A", r"(?i)\b4\s*BEDROOM\b.*TYPE\s*A(?!.*POOL)"),
    ("4BR-TYPE-B-POOL", r"(?i)\b4\s*BEDROOM\b.*TYPE\s*B.*(POOL|SWIMMING)"),
    ("5BR", r"(?i)\b5\s*BEDROOM\b")
]

def main():
    pages = load_pdf_pages(settings.PDF_PATH)
    # find first page indexes for each heading
    found = []
    for tag, pat in HEADINGS:
        idx = next((p["page"] for p in pages if re.search(pat, p["text"])), None)
        if idx: found.append((tag, idx))
    found.sort(key=lambda x: x[1])  # by page

    # list Rev11 images in name order
    imgs = sorted(
        [os.path.join(settings.IMAGES_DIR, f) for f in os.listdir(settings.IMAGES_DIR) if "Rev11" in f and f.endswith(".webp")]
    )

    # naive even split across groups in order
    groups = len(found) if found else 1
    chunk = max(1, len(imgs)//groups)
    mapping = {}
    for i,(tag,_) in enumerate(found):
        mapping[tag] = imgs[i*chunk:(i+1)*chunk]
    # put leftovers in the last group
    if found:
        mapping[found[-1][0]] = imgs[(groups-1)*chunk:]

    os.makedirs(os.path.dirname(settings.IMAGE_MAP_PATH), exist_ok=True)
    with open(settings.IMAGE_MAP_PATH, "w") as f:
        json.dump(mapping, f, indent=2)
    print(f"Wrote {settings.IMAGE_MAP_PATH}")

if __name__ == "__main__":
    main()
