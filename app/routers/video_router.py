from fastapi import APIRouter, File, UploadFile
import os
import uuid
import time
from app.core.detection_utils import process_video_file
from app.core.response_builder import build_response, log_event
from app.config import TEMP_DIR

router = APIRouter()

@router.post("/video-detect")
async def video_detect(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".webm")):
        return build_response([], "Unsupported file type", 1, 400)

    temp_path = os.path.join(TEMP_DIR, f"temp_{uuid.uuid4().hex}_{file.filename}")
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    log_event(f"Starting video detection for {file.filename}")
    start_ts = time.time()
    result = process_video_file(temp_path)
    os.remove(temp_path)
    log_event(f"Finished video detection in {time.time() - start_ts:.2f} sec")
    return build_response([result], "Processed video successfully")
