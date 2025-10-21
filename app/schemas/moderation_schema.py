from pydantic import BaseModel
from typing import List

class ImageInput(BaseModel):
    images: List[str]
