from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Initialize the OpenAI API with your API key

def transcribe_audio(audio_path):
    try:
        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return response.text
    except Exception as e:
        raise RuntimeError(f"OpenAI Whisper API transcription failed: {e}")
    

if __name__ == "__main__":
    audio_input =  r"C:\ai-avatar-sales-agent\backend\temp\audio\test_output1.wav"  # Specify your audio file here
    transcription = transcribe_audio(audio_input)
    print(f"Transcription: {transcription}")