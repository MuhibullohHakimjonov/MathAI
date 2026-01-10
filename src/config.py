import os
from dotenv import load_dotenv

load_dotenv()



# MINIMAX
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
MINIMAX_URL = "https://ollama.com/api/chat"
MINIMAX_MODEL = "gemini-3-flash-preview:cloud"
