from pydantic import BaseModel


class Class(BaseModel):
    id: int
    title: str
