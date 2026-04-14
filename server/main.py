import os
import uvicorn

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from routes.health import router as health_router
from routes.translate import router as translate_router
from routes.image import router as image_router
from routes.ner import router as ner_router
from routes.tts import router as tts_router

app = FastAPI(title="DA5402 A2 Multi-Modal Service", version="1.0.0")

app.include_router(ner_router)
app.include_router(health_router)
app.include_router(translate_router)
app.include_router(image_router)
app.include_router(tts_router)

if __name__ == "__main__":
    uvicorn.run(app, host=os.environ["HOST"], port=int(os.environ["PORT"]))