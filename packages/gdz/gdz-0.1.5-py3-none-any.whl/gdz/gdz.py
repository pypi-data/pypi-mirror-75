from typing import List

import requests

from .types.book import Book
from .types.class_ import Class
from .types.structure_entry import StructureEntry
from .types.subject import Subject
from .types.task import Task, ExtendedTask


class GDZ:
    API_ENDPOINT = "https://gdz-ru.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {"User-Agent": "okhttp/3.10.0"}
        self.main_info = self.session.get(self.API_ENDPOINT).json()

    @property
    def classes(self) -> List[Class]:
        return [Class(**external_data) for external_data in self.main_info["classes"]]

    @property
    def subjects(self) -> List[Subject]:
        return [
            Subject(**external_data) for external_data in self.main_info["subjects"]
        ]

    @property
    def books(self) -> List[Book]:
        return [Book(**external_data) for external_data in self.main_info["books"]]

    def book_structure(self, book: Book) -> List[StructureEntry]:
        structure = self.session.get(self.API_ENDPOINT + book.url).json()["structure"]
        return [StructureEntry(**external_data) for external_data in structure]

    def task_extended(self, task: Task) -> ExtendedTask:
        task_info = self.session.get(self.API_ENDPOINT + task.url).json()
        return ExtendedTask(**task_info)
