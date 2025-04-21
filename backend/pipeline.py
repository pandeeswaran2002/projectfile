import os
import uuid
import subprocess
from dotenv import load_dotenv
import openai
import pyttsx3
import torch
import cv2

# Load environment variables from .env file
load_dotenv()

# Set API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Model settings
MODEL = "llama3-70b-8192"

# Function 1: Audio Transcription (Whisper API)
def transcribe_audio(audio_path: str) -> str:
    try:
        with open(audio_path, "rb") as audio_file:
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )
        transcription = response['text']
        return transcription
    except Exception as e:
        raise RuntimeError(f"OpenAI Whisper API transcription failed: {e}")

# Function 2: AI Response Generation (Groq API)
def get_ai_response(user_message: str) -> str:
    from openai import OpenAI  # Use OpenAI API directly (Groq)
    client = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")

    try:
        response = client.chat.completions.create(
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
def text_to_speech(text: str, output_path: str = "temp/audio/test_output.wav") -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path

# Function 4: Image to Silent Video Conversion
def create_video_from_image(image_path, output_video_path, duration=5, fps=25, resolution=(640, 360)):
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Failed to read image: {image_path}")
        return False

    image = cv2.resize(image, resolution)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, resolution)

    for _ in range(int(duration * fps)):
        video_writer.write(image)

    video_writer.release()
    return True

# Function 5: Lip-Sync Video Generation (Wav2Lip)
def generate_lip_sync_from_image(image_path, audio_path, wav2lip_output_path):
    if not os.path.exists(image_path) or not os.path.exists(audio_path):
        print("❌ Image or audio not found.")
        return

    if not torch.cuda.is_available():
        print("⚠️ CUDA GPU not available. Running on CPU...")

    os.makedirs(os.path.dirname(wav2lip_output_path), exist_ok=True)

    silent_video_path = "temp/silent_video.mp4"
    success = create_video_from_image(image_path, silent_video_path)
    if not success:
        return

    command = [
        "python", "models/wav2lip/inference.py",
        "--checkpoint_path", "models/wav2lip/wav2lip.pth",
        "--face", silent_video_path,
        "--audio", audio_path,
        "--outfile", wav2lip_output_path
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error occurred:\n{result.stderr}")
    else:
        print(f"✅ Lip-sync video generated: {wav2lip_output_path}")

# Function 6: Mux Audio and Video (Final Output)
def mux_audio_video(video_path, audio_path, final_output_path):
    command = [
        'ffmpeg', '-y', '-i', video_path, '-i', audio_path,
        '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
        '-map', '0:v:0', '-map', '1:a:0', final_output_path
    ]
    subprocess.run(command)

# Main Pipeline Execution
def run_pipeline(audio_input: str, image_input: str):
    # Step 1: Transcribe the audio input
    transcription = transcribe_audio(audio_input)
    print(f"📝 Transcription: {transcription}")

    # Step 2: Get AI response from the transcription
    ai_response = get_ai_response(transcription)
    print(f"🤖 AI Response: {ai_response}")

    # Step 3: Convert AI response to speech (audio)
    audio_output = text_to_speech(ai_response, "temp/audio/response.wav")
    print(f"🎙️ Audio saved to: {audio_output}")

    # Step 4: Generate Lip-Sync Video using Wav2Lip
    video_id = str(uuid.uuid4())[:8]
    wav2lip_output = f"temp/video/response_{video_id}.mp4"
    generate_lip_sync_from_image(image_input, audio_output, wav2lip_output)

    # Step 5: Mux the audio and video together
    final_output = f"temp/video/final_{video_id}.mp4"
    mux_audio_video(wav2lip_output, audio_output, final_output)
    print(f"✅ Final video saved to: {final_output}")

if __name__ == "__main__":
    audio_input = "path_to_audio_file.wav"  # Update with the actual audio file path
    image_input = "path_to_image_file.jpg"  # Update with the actual image file path
    run_pipeline(audio_input, image_input)
