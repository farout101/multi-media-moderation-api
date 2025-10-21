import os
import torch

UNSAFE_LABELS = {"Adults", "Gambling", "Political", "Violence"}
SAFE_LABELS = [
    "Cultural", "Entertainment", "Environment",
    "Products", "Social", "Sports", "Technology"
]

YOLO_MODEL_PATH = r"models\yolooct11update.pt"
CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45
IMG_SIZE = 640
TEMP_DIR = "temp_media"
os.makedirs(TEMP_DIR, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
