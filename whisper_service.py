import os
import openai

# Initialize the OpenAI API with your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(audio_path: str) -> str:
    try:
        # Open the audio file in binary mode and send it to OpenAI API for transcription
        with open(audio_path, "rb") as audio_file:
            response = openai.Audio.transcribe(
                model="whisper-1",  # Use Whisper model for transcription
                file=audio_file
            )

        # Get the transcription from the response
        transcription = response['text']
        return transcription

    except Exception as e:
        raise RuntimeError(f"OpenAI Whisper API transcription failed: {e}")
