import os
import subprocess
import uuid

def generate_lip_sync(face_path, audio_path, output_path):
    # Ensure all paths are absolute
    face_path = os.path.abspath(face_path)
    audio_path = os.path.abspath(audio_path)
    output_path = os.path.abspath(output_path)

    # Check if the face and audio files exist
    if not os.path.exists(face_path):
        print(f"Error: Avatar video file not found at {face_path}")
        return

    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        return

    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Command to run Wav2Lip
    command = [
        "python", "models/wav2lip/inference.py",
        "--checkpoint_path", "models/wav2lip/wav2lip.pth",
        "--face", face_path,
        "--audio", audio_path,
        "--outfile", output_path
    ]
    
    # Print the command for debugging
    print(">> Running Wav2Lip with command:", " ".join(command))
    
    try:
        # Run the Wav2Lip command
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Check if there is any error
        if result.returncode != 0:
            print(f"Error occurred: {result.stderr}")
        else:
            print(f"Process finished successfully: {result.stdout}")
    except Exception as e:
        print(f"An error occurred while running Wav2Lip: {str(e)}")

if __name__ == "__main__":
    # Set paths to your avatar video, TTS audio, and the output video file
    face_path = "models/wav2lip/demo1.mp4"  # This should be the 2D or 3D avatar video path
    audio_file = "temp/audio/response_x.wav"  # The TTS output .wav file from Phase 5
    video_id = str(uuid.uuid4())[:8]  # Generate a unique ID for the video
    output_file = f"temp/video/response_{video_id}.mp4"  # Output video path

    # Call the lip sync function
    generate_lip_sync(face_path, audio_file, output_file)

