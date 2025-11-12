import threading
import numpy as np
from faster_whisper import WhisperModel
from scipy.signal import resample_poly # replace librosa for better speed but quality still good
import warnings
warnings.filterwarnings("ignore")

class VoiceTranscriptor:
    def __init__(self, model_name:str = "tiny.en"):
        self._model = WhisperModel(model_name)

    def transcribe(self, audio_bytes):
        audio_bytes = b"".join(audio_bytes)
        audio_bytes = np.frombuffer(audio_bytes, dtype = np.int16).astype(np.float32)/32768.0
        audio_bytes = resample_poly(audio_bytes, up=16000, down = 44100)
        segments, info = self._model.transcribe(audio_bytes)
        transcription = " ".join([segment.text for segment in segments])
        print(transcription)
        return transcription