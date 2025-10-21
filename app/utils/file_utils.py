import os
import uuid
from app.config import TEMP_DIR

def save_temp_file(upload_file):
    path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}_{upload_file.filename}")
    with open(path, "wb") as f:
        f.write(upload_file.file.read())
    return path
