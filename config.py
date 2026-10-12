from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

VIDEO_DIR = OUTPUT_DIR / "recordings"
VIDEO_DIR.mkdir(exist_ok=True)

DATABASE_PATH = BASE_DIR / "living_being.db"


# ============================================================
# YOLO
# ============================================================

MODEL_NAME = "yolo11n.pt"

CONFIDENCE_THRESHOLD = 0.40

IOU_THRESHOLD = 0.50


# ============================================================
# SUPPORTED LIVING BEINGS
# ============================================================

SUPPORTED_CLASSES = {
    "person",
    "dog",
    "cat",
    "cow",
    "bird",
}


# ============================================================
# DETECTION
# ============================================================

MAX_DETECTIONS = 50


# ============================================================
# MOVEMENT
# ============================================================

MOVEMENT_THRESHOLD = 15

RAPID_MOVEMENT_THRESHOLD = 80


# ============================================================
# FPS
# ============================================================

FPS_UPDATE_INTERVAL = 1.0


# ============================================================
# ALERTS
# ============================================================

RAPID_MOVEMENT_ALERT_ENABLED = True


# ============================================================
# ZONE
# ============================================================

DEFAULT_ZONE = {
    "x1": 0.10,
    "y1": 0.10,
    "x2": 0.90,
    "y2": 0.90,
}