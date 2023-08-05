import io
import os

from setuptools import find_packages, setup

NAME = "gdz"
DESCRIPTION = "Враппер API приложения ГДЗ: мой решебник (gdz.ru)"
URL = "https://github.com/crinny/gdz"
EMAIL = ""
AUTHOR = "crinny"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.1.5"

REQUIRED = ["requests", "pydantic"]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
