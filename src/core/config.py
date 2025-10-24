import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    PROVIDER = os.getenv("PROVIDER", "openai")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    PDF_PATH = os.getenv("PDF_PATH", "data/ABV Final Floorplans.pdf")
    IMAGES_DIR = os.getenv("IMAGES_DIR", "data/WebP")
    INDEX_DIR = os.getenv("INDEX_DIR", "storage/vector_index")
    IMAGE_MAP_PATH = os.getenv("IMAGE_MAP_PATH", "storage/image_map.json")

settings = Settings()
