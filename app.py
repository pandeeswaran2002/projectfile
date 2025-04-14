from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from tts_service import text_to_speech
import uuid
import os

app = FastAPI()

# ... your other routes like whisper, RAG, etc.

@app.post("/generate_audio")
async def generate_audio(request: Request):
    data = await request.json()
    text = data.get("text", "")

    if not text:
        return {"error": "Text input is required"}

    filename = f"response_{uuid.uuid4().hex[:8]}.wav"
    output_path = os.path.join("temp/audio", filename)

    text_to_speech(text, output_path)
    return FileResponse(output_path, media_type="audio/wav", filename=filename)
