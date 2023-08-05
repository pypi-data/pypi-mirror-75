from typing import List

from pydantic import BaseModel

from .book import Book
from .edition import Edition


class Task(BaseModel):
    title: str
    title_short: str
    description: str
    youtube_video_id: str
    url: str


class ExtendedTask(BaseModel):
    success: bool
    message: str
    paths: dict
    book: Book
    task: Task
    editions: List[Edition]
