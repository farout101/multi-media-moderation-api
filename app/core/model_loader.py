from ultralytics import YOLO
from .response_builder import log_event

from app.config import YOLO_MODEL_PATH

try:
    model = YOLO(YOLO_MODEL_PATH)
    log_event("Model loaded successfully.")
except Exception as e:
    raise RuntimeError(f"Failed to load YOLO model: {e}")
