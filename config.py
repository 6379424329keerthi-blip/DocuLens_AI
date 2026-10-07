import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
PROCESSED_DIR = DATA_DIR / "processed"
IMAGES_DIR = DATA_DIR / "images"

# Ensure dirs exist
for d in [UPLOAD_DIR, PROCESSED_DIR, IMAGES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def is_configured_key(key: str) -> bool:
    """Returns True if the key is real and not a template placeholder."""
    if not key:
        return False
    k = key.strip().lower()
    if "your" in k or k.startswith("sk-...") or len(key.strip()) < 15:
        return False
    return True

# API Keys & Models
_raw_gemini = os.getenv("GEMINI_API_KEY", "")
_raw_openai = os.getenv("OPENAI_API_KEY", "")

GEMINI_API_KEY = _raw_gemini if is_configured_key(_raw_gemini) else ""
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")

OPENAI_API_KEY = _raw_openai if is_configured_key(_raw_openai) else ""
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Determine active LLM provider
if GEMINI_API_KEY:
    ACTIVE_PROVIDER = "gemini"
elif OPENAI_API_KEY:
    ACTIVE_PROVIDER = "openai"
else:
    ACTIVE_PROVIDER = "local"

# Processing parameters
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
TEXT_THRESHOLD = 50  # chars/page below which we use OCR/vision
DEFAULT_DPI = 200
MAX_IMAGE_SIDE = 2048
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 5
CONFIDENCE_THRESHOLD = 0.7  # below this = low confidence
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
