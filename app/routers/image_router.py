from fastapi import APIRouter, File, UploadFile
from typing import List
import os
from app.schemas.moderation_schema import ImageInput
from app.core.detection_utils import process_image_file
from app.core.response_builder import build_response, log_event
from app.config import TEMP_DIR

router = APIRouter()

@router.post("/image-detect")
async def image_detect(input_data: ImageInput):
    results = []
    log_event(f"Starting image detection for {len(input_data.images)} images.")
    for img_path in input_data.images:
        if not os.path.exists(img_path):
            results.append({"image": img_path, "error": "File not found"})
            continue
        results.append(process_image_file(img_path))
    log_event("Finished image detection.")
    return build_response(results, "Processed images")

@router.post("/upload-image")
async def upload_and_detect_images(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        temp_path = os.path.join(TEMP_DIR, file.filename)
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        res = process_image_file(temp_path)
        results.append(res)
        os.remove(temp_path)
    return build_response(results, "Processed uploaded images")
