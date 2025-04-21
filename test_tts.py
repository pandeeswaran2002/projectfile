import pyttsx3

engine = pyttsx3.init()

text = (
    "Artificial Intelligence, or AI, refers to the simulation of human intelligence in machines that are "
    "programmed to think and learn like humans. It has a wide range of applications across different domains, "
    "including healthcare, education, finance, and transportation. AI enables systems to perform tasks such as "
    "speech recognition, decision-making, visual perception, and language translation. One of the key goals of AI "
    "research is to create systems that can function autonomously and adapt to new situations without explicit human instruction. "
    "With the rapid advancement of machine learning algorithms, access to big data, and powerful computational resources, "
    "AI technologies have evolved significantly over the past decade. While AI brings immense potential to transform industries, "
    "it also raises important ethical and societal concerns, such as job displacement, bias in decision-making, and data privacy. "
    "As we continue to integrate AI into our daily lives, it is crucial to develop responsible and transparent frameworks that ensure its safe and fair use."
)

# Save to a WAV file
engine.save_to_file(text, 'temp/audio/output1.wav')

# Run the engine to process the saving
engine.runAndWait()

print("✅ Speech saved to temp/audio/output1.wav")
