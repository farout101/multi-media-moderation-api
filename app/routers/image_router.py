from fastapi import APIRouter, File, UploadFile
from typing import List
import os
import asyncio
from app.schemas.moderation_schema import ImageInput
from app.core.detection_utils import process_image_file
from app.core.response_builder import build_response, log_event
from app.config import TEMP_DIR

router = APIRouter()

async def run_in_thread(func, *args):
    """Utility: run blocking function in threadpool"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)


@router.post("/image-detect")
async def image_detect(input_data: ImageInput):
    results = []
    log_event(f"Starting image detection for {len(input_data.images)} images.")

    async def process(img_path):
        if not os.path.exists(img_path):
            return {"image": img_path, "error": "File not found"}
        return await run_in_thread(process_image_file, img_path)

    # run all image processing concurrently
    results = await asyncio.gather(*[process(img) for img in input_data.images])

    log_event("Finished image detection.")
    return build_response(results, "Processed images")


@router.post("/upload-image")
async def upload_and_detect_images(files: List[UploadFile] = File(...)):
    results = []

    async def handle_file(file: UploadFile):
        temp_path = os.path.join(TEMP_DIR, file.filename)  # type: ignore
        # write the uploaded file to disk
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # process the image concurrently (thread-safe)
        res = await run_in_thread(process_image_file, temp_path)

        # remove the temp file
        os.remove(temp_path)
        return res

    # process all uploads concurrently
    results = await asyncio.gather(*[handle_file(file) for file in files])

    return build_response(results, "Processed uploaded images")
