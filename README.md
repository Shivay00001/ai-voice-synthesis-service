# ai-voice-synthesis-service

Real text-to-speech API: a FastAPI wrapper around a **real TTS HTTP API**
(ElevenLabs-compatible `POST /v1/text-to-speech/{voice_id}`). Returns genuine
MP3 audio bytes from the provider.

## What it does

- `POST /synthesize` — `{"text", "voice_id", "model_id"}` → `audio/mpeg` bytes
- `GET /voices` — real provider voice catalog
- `GET /health` — includes `key_configured`

## API key

| Env var              | Purpose                                  |
|----------------------|------------------------------------------|
| `ELEVENLABS_API_KEY` | **API key** for the TTS provider         |

Without the key, `/synthesize` returns **HTTP 503** with a clear message —
it never returns fake audio. With an invalid key, the provider's real 401 is
surfaced.

## Offline fallback (honest note)

There is no offline TTS in this service: real neural voices require the
provider API. If you need fully offline synthesis, install a local engine
(e.g. Coqui XTTS or Piper) and point this service's client at it — the
`synthesize()` function in `tts.py` is the single place to swap.

## Run

```bash
pip install -r requirements.txt
ELEVENLABS_API_KEY=... uvicorn main:app --port 8003
```

```bash
curl -X POST http://localhost:8003/synthesize -H 'Content-Type: application/json' \
  -d '{"text":"Hello from the voice service"}' --output speech.mp3
```

## Tests

```bash
python -m pytest tests/ -q
```

Covers: honest 503 without key, real upstream 401 with a dummy key (proves
the HTTP client is genuine), empty-text rejection.
