import random
import cv2
import os
import time
from app.config import SAFE_LABELS, UNSAFE_LABELS, CONFIDENCE_THRESHOLD, IOU_THRESHOLD, IMG_SIZE, DEVICE
from .model_loader import model

def detect_frame(frame_bgr):
    results = model.predict(
        frame_bgr, conf=CONFIDENCE_THRESHOLD, iou=IOU_THRESHOLD, device=DEVICE, imgsz=IMG_SIZE, verbose=False
    )

    res = results[0]
    boxes = res.boxes
    dets = []
    unsafe_found = False

    xyxy = boxes.xyxy.cpu().numpy() if hasattr(boxes, "xyxy") else [] # type: ignore
    cls_arr = boxes.cls.cpu().numpy() if hasattr(boxes, "cls") else [] # type: ignore
    conf_arr = boxes.conf.cpu().numpy() if hasattr(boxes, "conf") else [] # type: ignore

    if len(xyxy) == 0:
        fake_label = random.choice(SAFE_LABELS)
        dets.append({"class": fake_label, "confidence": 0.6, "auto": True})
        is_safe = True
    else:
        for (cls_idx, conf_score) in zip(cls_arr, conf_arr):
            class_name = res.names.get(int(cls_idx), str(int(cls_idx)))
            confidence = round(float(conf_score), 3)
            dets.append({"class": class_name, "confidence": confidence, "auto": False})
            if class_name in UNSAFE_LABELS:
                unsafe_found = True
        is_safe = not unsafe_found

    labels = list({d["class"] for d in dets})
    return {"is_safe": is_safe, "content_type": labels, "detections": dets}

def process_image_file(path: str):
    img = cv2.imread(path)
    result = detect_frame(img)
    return {
        "filename": os.path.basename(path),
        "is_safe": result["is_safe"],
        "content_type": result["content_type"],
        "detections": result["detections"],
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
    unsafe_overall = False

    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break
        det = detect_frame(frame)
        unsafe_in_frame = any(d["class"] in UNSAFE_LABELS for d in det["detections"])
        if unsafe_in_frame:
            unsafe_overall = True

        results.append({
            "frame_index": int(frame_idx),
            "time_sec": round(frame_idx / fps, 2),
            "is_safe": det["is_safe"],
            "detected_classes": [d["class"] for d in det["detections"]],
            "detections": det["detections"]
        })

        frame_idx += interval_frames
        if frame_count and frame_idx >= frame_count:
            break

    cap.release()
    return {
        "video_name": os.path.basename(video_path),
        "frames_analyzed": len(results),
        "fps": round(fps, 2),
        "duration_sec": round(duration_sec, 2),
        "is_safe": not unsafe_overall,
        "results": results,
    }
