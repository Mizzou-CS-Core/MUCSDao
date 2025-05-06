from setuptools import setup, find_packages

setup(
    name="mucs_database",
    version="0.7.2",
    packages=find_packages(),
    install_requires=[
        "peewee",
    ],
)
