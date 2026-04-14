import os
import html
from utils.id import get_container_id
from fastapi import APIRouter, HTTPException
from pydantic_schemas.translate import TranslateRequest, TranslateResponse
from .bhashini import Vaani

router = APIRouter()

vaani_nmt = Vaani(tasks="translation")


@router.post("/translate", response_model=TranslateResponse)
async def translate_text(req: TranslateRequest) -> TranslateResponse:
    text = req.text
    source_lang = req.source_language
    target_lang = req.target_language
    response = await vaani_nmt.translation(text, source_lang, target_lang)
    translated_text = response["pipelineResponse"][0]["output"][0]["target"]
    print(translate_text)
    return {"translated_text": translated_text, "container_id": get_container_id()}
