"""Real text-to-speech client (ElevenLabs-compatible HTTP API).

Reads the key from the environment. No key -> clear error, never fake audio.
"""
import os

import httpx

BASE_URL = "https://api.elevenlabs.io/v1"


class TTSError(Exception):
    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


def _key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not key:
        raise TTSError(
            "No API key configured. Set the ELEVENLABS_API_KEY environment variable "
            "to enable speech synthesis. Refusing to return fake audio."
        )
    return key


def synthesize(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM",
               model_id: str = "eleven_multilingual_v2",
               timeout: float = 60.0) -> bytes:
    """Real POST to /text-to-speech/{voice_id}; returns raw MP3 bytes."""
    resp = httpx.post(
        f"{BASE_URL}/text-to-speech/{voice_id}",
        headers={"xi-api-key": _key(), "Content-Type": "application/json",
                 "Accept": "audio/mpeg"},
        json={"text": text, "model_id": model_id,
              "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}},
        timeout=timeout,
    )
    if resp.status_code != 200:
        raise TTSError(
            f"TTS provider returned HTTP {resp.status_code}: {resp.text[:300]}",
            status=resp.status_code,
        )
    ctype = resp.headers.get("content-type", "")
    if "audio" not in ctype and len(resp.content) < 100:
        raise TTSError(f"Unexpected TTS response (content-type={ctype!r})")
    return resp.content


def list_voices(timeout: float = 30.0) -> list[dict]:
    """Real GET /voices; returns provider voice catalog."""
    resp = httpx.get(f"{BASE_URL}/voices",
                     headers={"xi-api-key": _key()}, timeout=timeout)
    if resp.status_code != 200:
        raise TTSError(
            f"TTS provider returned HTTP {resp.status_code}: {resp.text[:300]}",
            status=resp.status_code,
        )
    return resp.json().get("voices", [])
