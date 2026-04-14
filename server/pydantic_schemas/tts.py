from pydantic import BaseModel, Field
from typing import Optional


class TtsRequest(BaseModel):
    text: str
    language: str
    gender: str = 'male'

class TtsResponse(BaseModel):
    pass