import base64


def extract_math_from_image(image_path: str) -> str:
	with open(image_path, "rb") as f:
		image_base64 = base64.b64encode(f.read()).decode()
	return str(image_base64)
