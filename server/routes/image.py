import os
import requests
from fastapi import APIRouter, HTTPException
from utils.id import get_container_id
from pydantic_schemas.image import ImageGenRequest, ImageGenResponse

router = APIRouter()

IMAGE_API_URL = os.getenv("IMAGE_API_URL", "").strip()
IMAGE_API_KEY = os.getenv("IMAGE_API_KEY", "").strip()


@router.post("/image", response_model=ImageGenResponse)
async def image(req: ImageGenRequest):
    if not IMAGE_API_URL:
        raise HTTPException(status_code=500, detail="IMAGE_API_URL is not set")
    if not IMAGE_API_KEY:
        raise HTTPException(status_code=500, detail="IMAGE_API_KEY is not set")

    headers = {
        "Content-Type": "application/json",
        # fal Authorization
        "Authorization": f"Key {IMAGE_API_KEY}",
    }

    # give image_size as {width, height}
    payload = {
        "prompt": req.prompt,
        "image_size": {"width": req.width, "height": req.height},
        "num_images": 1,
    }

    try:
        r = requests.post(IMAGE_API_URL, json=payload, headers=headers, timeout=120)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Image provider error: {e}")

    # fal response
    images = data.get("images") or []
    urls = [
        img.get("url") for img in images if isinstance(img, dict) and img.get("url")
    ]

    if not urls:
        raise HTTPException(status_code=500, detail=f"No image url returned: {data}")

    return {"image_urls": urls, "container_id": get_container_id()}
