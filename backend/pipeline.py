import os
import uuid
import subprocess
from dotenv import load_dotenv
from openai import OpenAI
import pyttsx3
import torch
import cv2
from whisper_service import transcribe_audio
from pywav2lip import generate_lip_sync_from_image
from pywav2lip import mux_audio_video
from pywav2lip import create_video_from_image

# Load environment variables from .env file
load_dotenv()

# Set API keys
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
groq_client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

# Model settings
MODEL = "llama3-70b-8192"

# Function 1: Audio Transcription (Whisper API)
# Already handled in whisper_service.py (make sure it's updated for new OpenAI API)

# Function 2: AI Response Generation (Groq API)
def get_ai_response(user_message: str) -> str:
    try:
        response = groq_client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": "You are an FnI advisor."},
                      {"role": "user", "content": user_message}],
            temperature=0.7,
            max_tokens=512
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Function 3: Text-to-Speech Conversion (pyttsx3)
def text_to_speech(text: str, output_path: str = r"C:\ai-avatar-sales-agent\backend\temp\audio\test_output.wav") -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path





# Main Pipeline Execution
def run_pipeline(audio_input: str, image_input: str):
    # Step 1: Transcribe the audio input
    transcription = transcribe_audio(audio_input)
    print(f"📝 Transcription: {transcription}")

    # Step 2: Get AI response from the transcription
    ai_response = get_ai_response(transcription)
    print(f"🤖 AI Response: {ai_response}")

    # Step 3: Convert AI response to speech (audio)
    audio_output = text_to_speech(ai_response, r"C:\ai-avatar-sales-agent\backend\temp\audio\response.wav")
    print(f"🎙️ Audio saved to: {audio_output}")

    # Step 4: Generate Lip-Sync Video using Wav2Lip
    video_id = str(uuid.uuid4())[:8]
    wav2lip_output = rf"C:\ai-avatar-sales-agent\backend\temp\video\response_{video_id}.mp4"
    generate_lip_sync_from_image(image_input, audio_output, wav2lip_output)

    # Step 5: Mux the audio and video together
    final_output = rf"C:\ai-avatar-sales-agent\backend\temp\video\final_{video_id}.mp4"
    mux_audio_video(wav2lip_output, audio_output, final_output)
    print(f"✅ Final video saved to: {final_output}")

if __name__ == "__main__":
    audio_input = r"C:\ai-avatar-sales-agent\backend\temp\audio\test_output2.wav"
    image_input = r"C:\ai-avatar-sales-agent\backend\models\wav2lip\avatar.jpg"
    run_pipeline(audio_input, image_input)
