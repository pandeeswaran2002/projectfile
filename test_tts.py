# test_tts.py

from TTS.api import TTS

# Load the TTS model (you may need to adjust the model path or language)
model_name = "tts_models/en/ljspeech/tacotron2-DDC"
tts = TTS(model_name)

# Text to be converted to speech
text = "Hello, this pandeeswaran iam ai intern in nix wolves."

# Generate speech and save as a wav file
tts.tts_to_file(text=text, file_path="temp/audio/test_output.wav")

print("TTS output saved as test_output.wav")
