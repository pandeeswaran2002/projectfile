# backend/groq_chat.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

MODEL = "llama3-70b-8192"  # ✅ Updated model

def get_ai_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an FnI (Finance and Insurance) advisor helping customers with vehicle finance questions."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=512,
        )
        return {"response": response['choices'][0]['message']['content'].strip()}

    except openai.error.OpenAIError as e:
        return {"response": f"Error from Groq: {str(e)}"}

    except Exception as e:
        return {"response": f"Unexpected error: {str(e)}"}
