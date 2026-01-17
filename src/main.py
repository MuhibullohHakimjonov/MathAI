from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from router import solve

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

app = FastAPI()
handler = Mangum(app)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["https://main.dlsxjmlvwmbio.amplifyapp.com", "http://localhost:8080"],
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(solve.router)