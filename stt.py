from transformers import pipeline

# Load Whisper model from Hugging Face
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base"
)

def transcribe(audio_path):
    try:
        result = pipe(audio_path)
        return result["text"]
    except Exception as e:
        return f"STT Error: {str(e)}"