from typing import Optional
from pydantic import BaseModel


class SolutionResponse(BaseModel):
	solution: str


class ErrorResponse(BaseModel):
	error: str
	details: Optional[str] = None
