import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_URL = (
	"https://generativelanguage.googleapis.com/v1beta/models/"
	"gemini-2.5-flash:generateContent"
)


OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_URL = "https://ollama.com/api/chat"
OLLAMA_MODEL = "kimi-k2-thinking:cloud"
