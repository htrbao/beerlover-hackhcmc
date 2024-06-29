from pydantic import BaseModel

class UploadRes(BaseModel):
    success: bool
    results: list