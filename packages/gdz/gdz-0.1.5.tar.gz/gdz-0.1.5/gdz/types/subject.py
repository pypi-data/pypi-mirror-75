from pydantic import BaseModel


class Subject(BaseModel):
    id: int
    title: str
