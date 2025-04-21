from avatar_sync import generate_lip_synced_video

if __name__ == "__main__":
    audio_file = "response_1.wav"
    video_file = "output_1.mp4"
    generate_lip_synced_video(audio_file, video_file)
