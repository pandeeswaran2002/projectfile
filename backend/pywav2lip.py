import os
import subprocess
import uuid
import cv2
import torch

def create_video_from_image(image_path, output_video_path, duration=5, fps=25, resolution=(640, 360)):
    """Convert a static image into a silent video using OpenCV."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Failed to read image: {image_path}")
        return False

    # Resize to desired resolution
    image = cv2.resize(image, resolution)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, resolution)

    for _ in range(int(duration * fps)):
        video_writer.write(image)

    video_writer.release()
    print(f"✅ Created silent video from image: {output_video_path}")
    return True

def generate_lip_sync_from_image(image_path, audio_path, wav2lip_output_path):
    """Run Wav2Lip on an image and audio file to produce a silent video with lip-sync."""
    # Make paths absolute
    image_path = os.path.abspath(image_path)
    audio_path = os.path.abspath(audio_path)
    wav2lip_output_path = os.path.abspath(wav2lip_output_path)

    # Check file existence
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    if not os.path.exists(audio_path):
        print(f"❌ Audio not found: {audio_path}")
        return
    if not torch.cuda.is_available():
        print("⚠️ Warning: CUDA GPU not available. Wav2Lip will run slowly on CPU.")

    # Create required folders
    os.makedirs(os.path.dirname(wav2lip_output_path), exist_ok=True)

    # Step 1: Convert image to video
    silent_video_path = "temp/downscaled_face.mp4"
    success = create_video_from_image(image_path, silent_video_path)
    if not success:
        return

    # Step 2: Run Wav2Lip inference
    command = [
        "python", "models/wav2lip/inference.py",
        "--checkpoint_path", "models/wav2lip/wav2lip.pth",
        "--face", silent_video_path,
        "--audio", audio_path,
        "--outfile", wav2lip_output_path
    ]

    print("🎬 Running Wav2Lip with command:\n", " ".join(command))

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error occurred:\n{result.stderr}")
        else:
            print(f"✅ Lip-sync video generated: {wav2lip_output_path}")
    except Exception as e:
        print(f"❌ Exception during Wav2Lip run: {str(e)}")

def mux_audio_video(video_path, audio_path, final_output_path):
    """Mux the original audio with the Wav2Lip video output to ensure sound is included."""
    command = [
        'ffmpeg', '-y', '-i', video_path, '-i', audio_path,
        '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
        '-map', '0:v:0', '-map', '1:a:0',
        final_output_path
    ]
    print("🔄 Muxing audio and video:\n", " ".join(command))
    subprocess.run(command)

if __name__ == "__main__":
    # 🖼️ Input image of avatar (2D face)
    image_path = "models/wav2lip/avatar.jpg"

    # 🔊 Audio file (generated using TTS)
    audio_file = "temp/audio/test_outputcr7.wav"

    # 🆔 Generate unique video ID
    video_id = str(uuid.uuid4())[:8]

    # 🎥 Intermediate output (lip-sync without audio)
    wav2lip_output = f"temp/video/response_{video_id}.mp4"

    # 🎞️ Final output with audio
    final_output = f"temp/video/final_{video_id}.mp4"

    # Step 1: Generate silent lip-sync video
    generate_lip_sync_from_image(image_path, audio_file, wav2lip_output)

    # Step 2: Mux original audio into video
    mux_audio_video(wav2lip_output, audio_file, final_output)

    print(f"✅ Final video with audio is ready: {final_output}")
