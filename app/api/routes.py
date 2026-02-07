from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.tts_engine import tts_engine
from app.core.logging import logger
import os

router = APIRouter()

class SynthesisRequest(BaseModel):
    text: str
    voice_id: str | None = None

@router.post("/synthesize")
async def synthesize(request: SynthesisRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
        
    try:
        output_path = tts_engine.synthesize(request.text, voice_id=request.voice_id)
        return FileResponse(output_path, media_type="audio/wav")
    except Exception as e:
        logger.error(f"Synthesis failed: {e}")
        raise HTTPException(status_code=500, detail="Synthesis failed")

@router.get("/voices")
async def list_voices():
    # In a real app, we would list available voices from the engine
    return {"voices": [{"id": "default", "name": "Default Speaker", "language": "en"}]}
