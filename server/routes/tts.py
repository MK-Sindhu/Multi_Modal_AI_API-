import os
import base64
from .bhashini import Vaani
from datetime import datetime

from fastapi import APIRouter, HTTPException
from utils.id import get_container_id
from pydantic_schemas.tts import TtsRequest, TtsResponse

router = APIRouter()

vaani_tts = Vaani(tasks="tts")

@router.post("/tts")
async def tts(body: TtsRequest):
    text = body.text
    language = body.language
    gender = body.gender or "male"
    try:
        tts_output = await vaani_tts.tts(text, language, gender=gender)
        tts64 = tts_output["pipelineResponse"][0]["audio"][0]["audioContent"]
        wav_data = base64.b64decode(tts64)
    except Exception as e:
        return {"message": "Oops! something went wrong."}, 400
    with open(f"audio_{str(datetime.now())}.wav", 'wb') as f:
        f.write(wav_data)

    return {"text": text, "audio": {"format": "base64", "content": tts64}, "container_id": get_container_id()}
