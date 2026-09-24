"""Real text-to-speech API.

Thin FastAPI wrapper around a REAL TTS HTTP API (ElevenLabs-compatible).
Without an API key the service refuses honestly instead of returning fake
audio. See README for the offline fallback note.
"""
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from tts import TTSError, list_voices, synthesize

app = FastAPI(title="Voice Synthesis Service", version="1.0.0")


class SynthesizeRequest(BaseModel):
    text: str = Field(..., max_length=5000)
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # ElevenLabs "Rachel" default
    model_id: str = "eleven_multilingual_v2"


@app.get("/health")
def health():
    return {"status": "ok",
            "key_configured": bool(os.environ.get("ELEVENLABS_API_KEY"))}


@app.post("/synthesize")
def synthesize_speech(req: SynthesizeRequest):
    if not req.text.strip():
        raise HTTPException(400, "text must not be empty")
    try:
        audio = synthesize(req.text, req.voice_id, req.model_id)
    except TTSError as e:
        code = 503 if e.status is None else e.status
        raise HTTPException(code, str(e))
    return Response(content=audio, media_type="audio/mpeg",
                    headers={"Content-Disposition": 'attachment; filename="speech.mp3"'})


@app.get("/voices")
def voices():
    try:
        return {"voices": list_voices()}
    except TTSError as e:
        code = 503 if e.status is None else e.status
        raise HTTPException(code, str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8003)))
