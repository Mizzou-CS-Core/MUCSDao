from setuptools import setup, find_packages

setup(
    name="mucs_database",
    version="0.8.2.1",
    packages=find_packages(),
    install_requires=[
        "peewee",
        "deprecated"
    ],
)
