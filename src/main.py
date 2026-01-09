import os
import tempfile

from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import Optional
from src.model import SolutionResponse
from src.solver import solve_math


MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.post("/solve/", response_model=SolutionResponse)
async def solve(file: Optional[UploadFile] = File(None), task: Optional[str] = Form(None)):
	if not file and not task:
		raise HTTPException(
			status_code=400,
			detail="Please provide either a file or a text task"
		)
	try:
		temp_file_path = None

		if file:
			if not file.filename:
				raise HTTPException(
					status_code=400,
					detail="No file selected"
				)

			file_ext = Path(file.filename).suffix.lower()
			if file_ext not in ALLOWED_EXTENSIONS:
				raise HTTPException(
					status_code=400,
					detail="Only png, jpg, jpeg, webp supported"
				)

			content = await file.read()
			if len(content) > MAX_FILE_SIZE:
				raise HTTPException(
					status_code=400,
					detail=f"File too big. Maximum file size is {MAX_FILE_SIZE / 1024 / 1024}MB"
				)

			with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
				temp_file.write(content)
				temp_file_path = temp_file.name
		try:
			cleaned_task = None
			if task:
				cleaned_task = task.strip()
				if not cleaned_task:
					cleaned_task = None
				elif len(cleaned_task) > 5000:
					raise HTTPException(
						status_code=400,
						detail=f"Task too long. Maximum 5000 characters"
					)
			result = solve_math(cleaned_task, image_path=temp_file_path)

			if not result:
				raise HTTPException(
					status_code=422,
					detail=f"Task failed. Please try again later."
				)
			return SolutionResponse(solution=result)
		finally:
			if temp_file_path:
				try:
					os.unlink(temp_file_path)
				except Exception as e:
					print(e)
	except HTTPException:
		raise
	except Exception as e:
		print(f"Unexpected error in solve endpoint: {e}")
		raise HTTPException(
			status_code=500,
			detail="An error occurred while processing your request"
		)