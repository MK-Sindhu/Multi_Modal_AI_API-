from pydantic import BaseModel, Field
from typing import List


class NerRequest(BaseModel):
    text: str

class NerResponse(BaseModel):
    entity: str
    score: float
    index: int
    word: str
    start: int
    end: int

class NerListResponse(BaseModel):
    data: list[NerResponse]
    container_id: str

