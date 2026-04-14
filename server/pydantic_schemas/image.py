from pydantic import BaseModel, Field
from typing import List


class ImageGenRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    width: int = 1024
    height: int = 1024


class ImageGenResponse(BaseModel):
    image_urls: List[str]
    container_id: str
