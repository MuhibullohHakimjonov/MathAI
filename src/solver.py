import requests
from src.vision_extract import extract_math_from_image
from src.config import MINIMAX_API_KEY, MINIMAX_URL, MINIMAX_MODEL




def solve_math_text(problem: str) -> str:
	payload = {
		"model": MINIMAX_MODEL,
		"messages": [
			{
				"role": "system",
				"content": "You are a math tutor. Solve step by step clearly."
			},
			{
				"role": "user",
				"content": problem
			}
		],
		"stream": False
	}

	headers = {
		"Authorization": f"Bearer {MINIMAX_API_KEY}",
		"Content-Type": "application/json"
	}

	response = requests.post(
		MINIMAX_URL,
		json=payload,
		headers=headers,
		timeout=120
	)
	response.raise_for_status()

	return response.json()["message"]["content"]


def solve_math(task_text: str = None, image_path: str = None) -> str:
	if image_path:
		task_text = extract_math_from_image(image_path)
		print(task_text)

	if not task_text:
		return "No math problem provided"

	return solve_math_text(task_text)
