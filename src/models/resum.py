from pydantic import BaseModel


class Resum(BaseModel):
    id: str
    job_id: str
    content: str
    opnion: str
    file: str
    score: float  # Adicionando pontuação no arquivo também, se necessário