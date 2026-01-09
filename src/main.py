from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
from solver import solve_math

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.post("/solve/")
async def solve(file: UploadFile = None, task: str = Form(None)):
	if file:
		file_path = f"/tmp/{file.filename}"
		with open(file_path, "wb") as buffer:
			shutil.copyfileobj(file.file, buffer)
		result = solve_math(image_path=file_path)

	elif task:
		result = solve_math(task_text=task)

	else:
		result = "Please provide a file or a text task."

	return {"solution": result}
