import pyaudio
import threading
import warnings
warnings.filterwarnings("ignore")


class VoiceRecorder:
    def __init__(self, FORMAT = pyaudio.paInt16,
                 CHANNELS:int = 1,
                 RATE:int = 44100,
                 CHUNK:int = 1024,
                 width:int = 2):
        
        self._FORMAT = FORMAT
        self._CHANNELS = CHANNELS
        self._RATE = RATE
        self._CHUNK = CHUNK
        self._audio = pyaudio.PyAudio()
        self._frames = []
        self._recording = False
        self._thread = None
        self._WIDTH = width

    def _record_loop(self):
        stream = self._audio.open(
            format = self._FORMAT,
            channels = self._CHANNELS,
            rate = self._RATE,
            frames_per_buffer = self._CHUNK,
            input = True
        )
        self._frames.clear()
        while self._recording:
            try:
                data = stream.read(self._CHUNK, exception_on_overflow = False)
                self._frames.append(data)
            except Exception as e:
                print("exception in record:",e)
                break
        stream.stop_stream()
        stream.close()

    def start(self):
        if self._recording:
            print("already recording")
            return
        self._recording = True
        self._thread = threading.Thread(target = self._record_loop, daemon = True)
        self._thread.start()
        print("recording started...")

    def stop(self):
        if not self._recording:
            print("Not recording")
            return
        self._recording = False
        self._thread.join()
        print("recording stopped.")

    def get_audio(self):
        if not self._frames:
            print("No audio recorded")
            return
        return self._frames

    def close(self):
        self._audio.terminate()

    def play_audio(self, audio_bytes):
        
        stream = self._audio.open(format=self._audio.get_format_from_width(self._WIDTH),
                                  rate=self._RATE,
                                  channels=self._CHANNELS,
                                  output=True)
        stream.write(audio_bytes)

if __name__ == "__main__":
    recorder = VoiceRecorder()
    input("Press enter to start recording...")
    recorder.start()
    input("Press enter to stop recording...")
    recorder.stop()
    audio_data = recorder.get_audio()
    audio_bytes = b"".join(audio_data)
    recorder.play_audio(audio_bytes=audio_bytes)
    recorder.close()