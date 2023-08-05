# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="django-translate2",
    version="1.0.20",
    author="Adam Zieliński",
    author_email="adam@adamziel.com",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/haimmag/django_translate",

    license="MIT",
    description="Non-gettext translations for django.",

    # Dependent packages (distributions)
    install_requires=[
        "python_translate"
    ],
)
