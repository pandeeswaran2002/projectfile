import os
from TTS.api import TTS

# Load the TTS model (do this once to avoid reloading every time)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)


def text_to_speech(text: str, output_path: str):
    """
    Generate TTS audio from text and save it to the given path.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate and save the speech
    tts.tts_to_file(text=text, file_path=output_path)
