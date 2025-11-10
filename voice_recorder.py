import os
import wave
import pyaudio
import librosa
import whisper
import threading
import numpy as np
from faster_whisper import WhisperModel
import warnings
warnings.filterwarnings("ignore")

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNKS = 1024 # frames_per_buffer
p = pyaudio.PyAudio()

recording = False
model = whisper.load_model("small.en")  # use tiny.en, small.en, or base.en for English-only
frames = []
def record():
    global frames
    stream = p.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        frames_per_buffer = CHUNKS,
        input = True
    )
    # frames = []
    frames.clear()
    while recording:
        try:
            data = stream.read(
            CHUNKS,
            exception_on_overflow = False)
            
            data = np.frombuffer(data, dtype=np.int16).astype(np.float32)/32768.0
            data = librosa.resample(data, orig_sr=44100, target_sr=16000)
            frames.append(data)
        except Exception as e:
            print(e)
            break
    stream.stop_stream()
    stream.close()

if __name__ == "__main__":
    input("Enter to start the recording: ")
    recording = True
    task = threading.Thread(target = record, daemon = True)
    task.start()
    try:
        input()
    except KeyboardInterrupt:
        print("exception")
    finally:
        recording =False
        task.join()
        p.terminate()
        print(len(frames))
        if frames:
            frame = np.concatenate(frames)
            result = model.transcribe(frame, language='english')
            print(result.get("text"))