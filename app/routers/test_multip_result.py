from fastapi import APIRouter, File, UploadFile
import os
import uuid
import time
from app.core.detection_utils import process_video_file
from app.core.response_builder import build_response, log_event
from app.config import TEMP_DIR

import asyncio

router = APIRouter()

async def run_in_thread(func, *args):
    """Utility: run blocking function in threadpool"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)

@router.post("/production-video-detect")
async def video_detect_production(file: UploadFile = File(...)):
    results = []
    if not file.filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".webm")): # type: ignore
        return build_response([], "Unsupported file type", 1, 400)

    temp_path = os.path.join(TEMP_DIR, f"temp_{uuid.uuid4().hex}_{file.filename}")
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    log_event(f"Starting video detection for {file.filename}")
    start_ts = time.time()

    for _ in range(10):  # Simulate some production-specific processing
        result = await run_in_thread(process_video_file, temp_path)
        results.append(result)

    os.remove(temp_path)
    log_event(f"Finished video detection in {time.time() - start_ts:.2f} sec")
    return build_response(results, "Processed video successfully")