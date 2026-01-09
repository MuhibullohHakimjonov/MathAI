import requests
from src.vision_extract import extract_math_from_image
from src.config import MINIMAX_API_KEY, MINIMAX_URL, MINIMAX_MODEL
from src.prompts import prompt_for_kimi




def send_request_to_kimi(problem: str) -> str:
	payload = {
		"model": MINIMAX_MODEL,
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
		"stream": False
	}

	headers = {
		"Authorization": f"Bearer {MINIMAX_API_KEY}",
		"Content-Type": "application/json"
	}
	try:
		response = requests.post(
			MINIMAX_URL,
			json=payload,
			headers=headers,
			timeout=120
		)
		print(f'Response from Kimi: {response.text}')
		response.raise_for_status()

		return response.json()["message"]["content"]
	except Exception as e:
		print(e)


def solve_math(task_text: str = None, image_path: str = None) -> str:
	extracted_text = None
	if image_path:
		extracted_text = extract_math_from_image(image_path)
		print(f'Extracted text from image: {extracted_text}')

	if extracted_text and task_text:
		combined_problem = f"Image content: {extracted_text}\n\nText content: {task_text}"

	elif extracted_text:
		combined_problem = extracted_text

	elif task_text:
		combined_problem = task_text
	else:
		return "No problem to solve"

	print(f'Request to kimi: {combined_problem}')

	return send_request_to_kimi(combined_problem)