import threading
import numpy as np
from faster_whisper import WhisperModel
from scipy.signal import resample_poly # replace librosa for better speed but quality still good
import warnings
from ollama import chat
warnings.filterwarnings("ignore")


###########
##########
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io
###########

class VoiceTranscriptor:
    def __init__(self, model_name:str = "tiny.en"):
        self._model = WhisperModel(model_name)

    def transcribe(self, audio_bytes):
        audio_bytes = b"".join(audio_bytes)
        audio_bytes = np.frombuffer(audio_bytes, dtype = np.int16).astype(np.float32)/32768.0
        audio_bytes = resample_poly(audio_bytes, up=16000, down = 44100)
        segments, info = self._model.transcribe(audio_bytes)
        transcription = " ".join([segment.text for segment in segments])
        return transcription
    
    def get_answer(self, question):
        resp = chat(
            model="deepseek-r1:1.5b",                # exact model name (see notes below)
            messages=[
                {"role": "system", "content": "You are a telecall assistance that answers concise and politely"},
                {"role": "user", "content": question}
                ]
        )
        return resp.message.content
    
    def text_to_audio(self, text):
        tts = gTTS(text=text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        sound = AudioSegment.from_file(mp3_fp, format="mp3")
        play(sound)