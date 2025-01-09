from pydantic import BaseModel

class File(BaseModel):
    file_id: str
    job_id: str
    score: float  # Campo para armazenar a pontuação calculada