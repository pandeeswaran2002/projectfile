# backend/groq_chat.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "llama3-70b-8192"

def get_ai_response(user_message):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an FnI (Finance and Insurance) advisor helping customers with vehicle finance questions."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=512,
        )
        return {"response": response.choices[0].message.content.strip()}

    except Exception as e:
        return {"response": f"Unexpected error: {str(e)}"}


if __name__ == "__main__":
    # You can change the question here if you like
    user_input = "What are the benefits of getting vehicle insurance directly from a dealership?"
    result = get_ai_response(user_input)
    print("🤖 Groq AI:", result["response"])