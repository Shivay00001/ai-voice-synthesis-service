import torch
from TTS.api import TTS
from app.core.config import settings
from app.core.logging import logger
import os
import uuid

class TTSEngine:
    def __init__(self):
        self.model_name = settings.DEFAULT_MODEL_NAME
        self.device = "cuda" if settings.USE_GPU and torch.cuda.is_available() else "cpu"
        self.tts = None
        
    def load(self):
        if self.tts is None:
            logger.info(f"Loading TTS model: {self.model_name} on {self.device}")
            self.tts = TTS(self.model_name, progress_bar=False).to(self.device)
            
    def synthesize(self, text: str, voice_id: str = None) -> str:
        self.load()
        
        if not os.path.exists(settings.OUTPUT_FOLDER):
            os.makedirs(settings.OUTPUT_FOLDER)
            
        filename = f"{uuid.uuid4()}.wav"
        output_path = os.path.join(settings.OUTPUT_FOLDER, filename)
        
        logger.info(f"Synthesizing text: {text[:50]}...")
        # For simplicity, we use the default speaker if voice_id is not provided
        self.tts.tts_to_file(text=text, file_path=output_path)
        
        return output_path

tts_engine = TTSEngine()
