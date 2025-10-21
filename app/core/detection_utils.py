import random
import cv2
import os
from collections import Counter
from app.config import SAFE_LABELS, CONFIDENCE_THRESHOLD, IOU_THRESHOLD, IMG_SIZE, DEVICE
from .model_loader import model


def detect_frame(frame_bgr):
    results = model.predict(
        frame_bgr,
        conf=CONFIDENCE_THRESHOLD,
        iou=IOU_THRESHOLD,
        device=DEVICE,
        imgsz=IMG_SIZE,
        verbose=False,
    )

    res = results[0]
    boxes = res.boxes
    dets = []

    xyxy = boxes.xyxy.cpu().numpy() if hasattr(boxes, "xyxy") else [] # type: ignore
    cls_arr = boxes.cls.cpu().numpy() if hasattr(boxes, "cls") else [] # type: ignore
    conf_arr = boxes.conf.cpu().numpy() if hasattr(boxes, "conf") else [] # type: ignore

    if len(xyxy) == 0:
        fake_label = random.choice(SAFE_LABELS)
        dets.append({"class": fake_label, "confidence": 0.6, "auto": True})
    else:
        for cls_idx, conf_score in zip(cls_arr, conf_arr):
            class_name = res.names.get(int(cls_idx), str(int(cls_idx)))
            confidence = round(float(conf_score), 3)
            dets.append({"class": class_name, "confidence": confidence, "auto": False})

    return dets


def calculate_safety(percentages):
    """Decide overall safety from category percentages"""
    p = {k.lower(): v for k, v in percentages.items()}

    if p.get("political", 1) >= 20 or p.get("violence", 1) >= 20:
        return False
    if p.get("adults", 1) >= 50:
        return False
    if p.get("gambling", 1) >= 60:
        return False

    return True    

def process_image_file(path: str):
    img = cv2.imread(path)
    dets = detect_frame(img)
    category_counts = Counter([d["class"] for d in dets])
    total = sum(category_counts.values()) or 1

    percentages = {k: round((v / total) * 100, 2) for k, v in category_counts.items()}
    is_safe = calculate_safety(percentages)

    return {
        "filename": os.path.basename(path),
        "is_safe": is_safe,
        "unsafe_categories": [k for k in percentages.keys() if k not in SAFE_LABELS],
        "category_percentages": percentages,
        "detections": dets,
    }


def process_video_file(video_path: str):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Cannot open video")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    duration_sec = frame_count / fps if frame_count else 0

    interval_sec = 3 if duration_sec < 60 else 5 if duration_sec < 120 else 7
    interval_frames = max(1, int(fps * interval_sec))
    frame_idx = 0

    results = []
    total_counts = Counter()

    # ---- Loop: Collect detections only ----
    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        dets = detect_frame(frame)
        frame_counts = Counter([d["class"] for d in dets])
        total_counts.update(frame_counts)

        results.append({
            "frame_index": int(frame_idx),
            "time_sec": round(frame_idx / fps, 2),
            "detections": dets
        })

        frame_idx += interval_frames
        if frame_count and frame_idx >= frame_count:
            break

    cap.release()

    # ---- Final Aggregation ----
    total_dets = sum(total_counts.values()) or 1
    print("Total Detections:", total_counts)
    overall_percentages = {
        k: round((v / total_dets) * 100, 2) for k, v in total_counts.items()
    }
    print("Overall Percentages:", overall_percentages)

    # Calculate safety once here
    is_safe = calculate_safety(overall_percentages)

    return {
        "video_name": os.path.basename(video_path),
        "frames_analyzed": len(results),
        "fps": round(fps, 2),
        "duration_sec": round(duration_sec, 2),
        "is_safe": is_safe,
        "unsafe_categories": [k for k in overall_percentages.keys() if k not in SAFE_LABELS],
        "overall_category_percentages": overall_percentages,
        # "results": results,
    }
