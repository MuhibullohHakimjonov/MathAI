import base64

import requests
from src.config import GEMINI_API_KEY, GEMINI_URL


def extract_math_from_image(image_path: str) -> str:
	with open(image_path, "rb") as f:
		image_base64 = base64.b64encode(f.read()).decode()

	payload = {
		"contents": [
			{
				"parts": [
					{
						"text": (
							"Extract the whole text from this image as plain text."
							"Do NOT solve it. Return only the problem."
						)
					},
					{
						"inline_data": {
							"mime_type": "image/png",
							"data": image_base64
						}
					}
				]
			}
		]
	}
	try:
		response = requests.post(
			f"{GEMINI_URL}?key={GEMINI_API_KEY}",
			json=payload,
			timeout=120
		)
		print(f'Response from gemini: {response.text}')
		response.raise_for_status()

		return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip(), 200
	except Exception as e:
		print(e)