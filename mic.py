import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename="mic_input.wav", duration=10, fs=44100):
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, recording)
    return filename