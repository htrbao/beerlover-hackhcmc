from pydantic import BaseModel

class VotingRes(BaseModel):
    success: bool
    results: list