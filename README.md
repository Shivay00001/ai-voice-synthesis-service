# AI Voice Synthesis Service

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com/)
[![TTS](https://img.shields.io/badge/CoquiTTS-0.22-green.svg)](https://github.com/coqui-ai/TTS)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **production-grade Text-to-Speech (TTS) service** providing high-quality voice synthesis via a robust API. Designed for low-latency synthesis and easy integration into applications.

## 🚀 Features

- **High Fidelity**: Leverages state-of-the-art TTS models (VITS, YourTTS).
- **Multiple Voices**: Support for various speakers and languages.
- **RESTful API**: Simple endpoints for synthesis and voice listing.
- **Real-time Streaming**: Support for streaming audio output.
- **Caching**: Intelligent caching of synthesized audio for repeated text.
- **Containerized**: Ready for deployment with Docker.

## 📁 Project Structure

```
ai-voice-synthesis-service/
├── app/
│   ├── api/          # API route handlers
│   ├── core/         # Configuration and logger
│   ├── services/     # TTS engine integration
│   └── main.py       # Application entrypoint
├── tests/            # Unit and functional tests
├── Dockerfile        # Production build
├── docker-compose.yml# Local development setup
└── requirements.txt  # Project dependencies
```

## 🛠️ Quick Start

```bash
# Clone
git clone https://github.com/Shivay00001/ai-voice-synthesis-service.git

# Set up environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📄 License

MIT License
