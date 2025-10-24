import os, json
from src.core.config import settings

def load_image_map():
    if not os.path.exists(settings.IMAGE_MAP_PATH):
        return {}
    with open(settings.IMAGE_MAP_PATH, "r") as f:
        return json.load(f)

def find_images_for(villa_tags, image_map):
    # villa_tags is list like ["4BR-TYPE-B-POOL"] -> return paths
    for tag in villa_tags:
        if tag in image_map:
            return [{"path": p, "description": f"{tag} floorplan", "relevance":"floorplan"} for p in image_map[tag]]
    # fallback: nothing
    return []
