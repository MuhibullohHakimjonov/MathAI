import os
import tempfile
from typing import Optional
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, Form, File, Request

from model import SolutionResponse
from utils.solver import solve_math
from db.supabase import check_rate_limit, insert_check_logs
from utils.get_ip import get_client_ip_from_lambda

router = APIRouter(
	prefix="/solve",
	tags=["solve"],
	responses={404: {"description": "Not found"}},
)


@router.post("", response_model=SolutionResponse)
async def solve(request: Request, file: Optional[UploadFile] = File(None), task: Optional[str] = Form(None)):
	ip = get_client_ip_from_lambda(request)
	print(f'user ip: {ip}')
	is_allowed = check_rate_limit(ip)
	if is_allowed != True:
		raise HTTPException(
			status_code=400,
			detail=f"Rate limit exceeded: {is_allowed}"
		)

	insert_user_request = insert_check_logs(ip)
	print(insert_user_request)

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
			from main import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
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
