import os
from dotenv import load_dotenv

load_dotenv()

# GEMINI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_URL = (
	"https://generativelanguage.googleapis.com/v1beta/models/"
	"gemini-2.5-flash:generateContent"
)

# MINIMAX
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
MINIMAX_URL = "https://ollama.com/api/chat"
MINIMAX_MODEL = "kimi-k2-thinking:cloud"
