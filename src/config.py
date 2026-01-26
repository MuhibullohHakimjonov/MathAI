import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = (
	f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
)

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_URL = "https://ollama.com/api/chat"
OLLAMA_MODEL = "kimi-k2-thinking:cloud"


SUPABASE_URL= os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY='sb_publishable_Vz-BAaULEiSajh5A21b8IA_aCycdUP_'
SUPABASE_SECRET_KEY= os.getenv('SUPABASE_SECRET_KEY')