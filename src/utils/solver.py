"""
AI Math Solver - Handles communication with Kimi API
"""
import requests
import os
from typing import Optional, Generator
from config import OLLAMA_API_KEY, OLLAMA_URL, OLLAMA_MODEL
from prompts import prompt_for_kimi
from utils.vision_extract import extract_math_from_image


def solve_math_streaming(task_text: Optional[str] = None, image_path: Optional[str] = None) -> Generator[
	bytes, None, None]:
	try:
		# Extract text from image if provided
		extracted_text = None
		if image_path:
			extracted_text = extract_math_from_image(image_path)

		# Combine problem from multiple sources
		combined_problem = _combine_problem(task_text, extracted_text)
		print(f'Request to kimi: {combined_problem}')

		# Stream the response from Kimi
		yield from _stream_kimi_response(combined_problem)

	finally:
		# Always clean up the temp file
		if image_path and os.path.exists(image_path):
			try:
				os.unlink(image_path)
				print(f'Cleaned up temp file: {image_path}')
			except Exception as e:
				print(f'Error deleting temp file: {e}')


def _combine_problem(task_text: Optional[str], extracted_text: Optional[str]) -> str:
	"""Combine task text and extracted text into a single problem statement."""
	if extracted_text and task_text:
		return f"Image text: {extracted_text}\n\nUser prompt: {task_text}"
	elif extracted_text:
		return extracted_text
	elif task_text:
		return task_text
	else:
		return "No problem to solve"


def _stream_kimi_response(problem: str) -> Generator[bytes, None, None]:
	payload = {
		"model": OLLAMA_MODEL,
		"messages": [
			{
				"role": "system",
				"content": prompt_for_kimi
			},
			{
				"role": "user",
				"content": str(problem)
			}
		],
		"stream": True
	}

	headers = {
		"Authorization": f"Bearer {OLLAMA_API_KEY}",
		"Content-Type": "application/json"
	}

	try:
		response = requests.post(
			OLLAMA_URL,
			json=payload,
			headers=headers,
			timeout=120,
			stream=True
		)
		response.raise_for_status()

		# Stream each line to the client
		for line in response.iter_lines():
			if line:
				try:
					yield line + b'\n'
				except Exception as e:
					print(f'Error streaming chunk: {e}')
					continue

	except requests.exceptions.RequestException as e:
		print(f'Error connecting to Kimi API: {e}')
		# Send error as NDJSON
		error_response = {
			"error": True,
			"message": "Failed to connect to AI service",
			"done": True
		}
		import json
		yield json.dumps(error_response).encode('utf-8') + b'\n'
	except Exception as e:
		print(f'Unexpected error in Kimi request: {e}')
		error_response = {
			"error": True,
			"message": "An unexpected error occurred",
			"done": True
		}
		import json
		yield json.dumps(error_response).encode('utf-8') + b'\n'


# Optional: Non-streaming version for backward compatibility
def solve_math(task_text: Optional[str] = None, image_path: Optional[str] = None) -> str:
	import json

	thinking_text = ""
	content_text = ""

	try:
		for chunk in solve_math_streaming(task_text, image_path):
			try:
				data = json.loads(chunk.decode('utf-8'))

				if data.get("message"):
					if data["message"].get("thinking"):
						thinking_text += data["message"]["thinking"]
					if data["message"].get("content"):
						content_text += data["message"]["content"]

				if data.get("done"):
					break

			except json.JSONDecodeError:
				continue

	except Exception as e:
		print(f'Error in non-streaming solve: {e}')
		return "Failed to generate solution"

	return content_text if content_text else "No response generated"