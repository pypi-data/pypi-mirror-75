from typing import List

from pydantic import BaseModel

from gdz.types.task import Task


class StructureEntry(BaseModel):
    title: str
    title_short: str
    description: str
    tasks: List[Task]
    topics: list
