from typing import List

from pydantic import BaseModel


class Cover(BaseModel):
    title: str
    url: str


class Price(BaseModel):
    purchase: int
    download: int


class Book(BaseModel):
    id: int
    parent_id: int
    country: str
    subject_id: int
    title: str
    header: str
    breadcrumb: str
    year: str
    classes: List[int]
    authors: List[str]
    authors_ru: List[str]
    authors_en: List[str]
    authors_by: List[str]
    authors_ua: List[str]
    description: str
    publisher: str
    category: str
    series: str
    subtype: str
    study_level: str
    parts: list
    cover: Cover
    cover_url: str
    search_keywords: str
    price: Price
    tasks_view: str
    is_paid: bool
    url: str
    priority: int
    updated_at: int
