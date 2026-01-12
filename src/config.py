import os
from dotenv import load_dotenv

load_dotenv()



OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_URL = "https://ollama.com/api/chat"
OLLAMA_MODEL = "kimi-k2-thinking:cloud"
