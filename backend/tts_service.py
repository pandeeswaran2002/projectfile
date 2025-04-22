import os
import pyttsx3

def text_to_speech(text: str, output_path: str = "temp/audio/test_output.wav") -> str:
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)  # Make sure this is a file, not a folder
    engine.runAndWait()
    
    return output_path

if __name__ == "__main__":
    sample_text = "Explain Artificial Intelligence (AI) in simple terms. What is it, how does it work, and what are its main applications in today's world? Include information on its types (Narrow AI vs. General AI), key techniques like Machine Learning and Deep Learning, and common use cases in industries like healthcare, transportation, and entertainment."
    output_file = "temp/audio/test_output1.wav"
    path = text_to_speech(sample_text, output_file)
    print(f"✅ Audio saved to: {path}")
