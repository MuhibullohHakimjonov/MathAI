from pydantic import BaseModel


class SolutionResponse(BaseModel):
	solution: str

