from pydantic import BaseModel, Field
from typing import Optional


class TranslateRequest(BaseModel):
    text: str = Field(..., min_lenght=1)
    source_language: str
    target_language: str = Field(..., description="Language code like en, hi, fr")


class TranslateResponse(BaseModel):
    translated_text: str
    container_id: str
