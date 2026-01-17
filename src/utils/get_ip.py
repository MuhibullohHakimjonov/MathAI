from fastapi import Request


def get_client_ip_from_lambda(request: Request) -> str:
	"""
	Extract client IP from Lambda event (for AWS Amplify + Lambda)
	"""
	# Get the raw AWS event from request
	if hasattr(request, "scope") and "aws.event" in request.scope:
		event = request.scope["aws.event"]

		# Try to get IP from different sources
		headers = event.get("headers", {})

		# CloudFront headers
		if headers.get("CloudFront-Viewer-Address"):
			# Format: "192.0.2.1:443"
			viewer_address = headers["CloudFront-Viewer-Address"]
			ip = viewer_address.split(":")[0]
			return ip

		# X-Forwarded-For from CloudFront
		x_forwarded_for = headers.get("X-Forwarded-For")
		if x_forwarded_for:
			return x_forwarded_for.split(",")[0].strip()

		# API Gateway context
		request_context = event.get("requestContext", {})
		if "identity" in request_context:
			identity = request_context["identity"]
			# API Gateway V1
			if "sourceIp" in identity:
				return identity["sourceIp"]
			# API Gateway V2
			if "http" in request_context:
				source_ip = request_context["http"].get("sourceIp")
				if source_ip:
					return source_ip

	# Fallback to request.client.host (might be Lambda's IP)
	return request.client.host if request.client else "unknown"
