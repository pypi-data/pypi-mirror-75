# gdz
Враппер API приложения [ГДЗ: мой решебник](https://play.google.com/store/apps/details?id=com.gdz_ru).

<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">

## Установка
```sh
pip install gdz
``` 

## Пример
```python
from gdz import GDZ

gdz = GDZ()

for book in gdz.books:
    if book.title == "Математика 5 класс Виленкин Н.Я. (2018 год)":
        print(book.description)
```
