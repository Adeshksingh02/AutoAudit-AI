import os
import google.generativeai as genai
from dotenv import load_dotenv

# Environment variables load karein
load_dotenv()

# Gemini API ko configure karein
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("⚠️ WARNING: GEMINI_API_KEY not found in .env file!")

class BaseAgent:
    def __init__(self, name: str, role_prompt: str):
        self.name = name
        self.role_prompt = role_prompt
        # Hum gemini-1.5-flash use karenge kyunki yeh fast aur efficient hai
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def think_and_act(self, user_input: str) -> str:
        """Yeh function agent ko 'Reasoning' (sochne) ki taqat deta hai."""
        full_prompt = f"Role: {self.role_prompt}\n\nTask: {user_input}"
        try:
            print(f"[{self.name}] Thinking...")
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            error_msg = f"Error executing task: {str(e)}"
            print(f"[{self.name}] ❌ {error_msg}")
            return error_msg