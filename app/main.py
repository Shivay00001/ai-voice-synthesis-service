from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    # Pre-load the model to avoid latency on first request
    # This might be slow depending on the environment, 
    # but good for production-readiness.
    from app.services.tts_engine import tts_engine
    # tts_engine.load() # Commented out for now to speed up initial test runs
    pass
