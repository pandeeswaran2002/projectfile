import sys
import os

# Add the current directory (backend) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.groq_chat import get_ai_response

# Now, you can call the function
result = get_ai_response("what is ai??")
print(result)
