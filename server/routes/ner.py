import os
from fastapi import APIRouter, HTTPException
from utils.id import get_container_id
from pydantic_schemas.ner import NerRequest, NerListResponse

router = APIRouter()

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

ner_model = os.getenv("TRANSFORMER_NER_MODEL", "").strip()

@router.post("/ner", response_model=NerListResponse)
def ner(body: NerRequest):
    text = body.text

    tokenizer = AutoTokenizer.from_pretrained(ner_model)
    model = AutoModelForTokenClassification.from_pretrained(ner_model)

    nlp = pipeline("ner", model=model, tokenizer=tokenizer)

    ner_results = nlp(text)
    for res in ner_results:
        res["score"] = float(res["score"])
    return {"data": ner_results,  "container_id": get_container_id()}