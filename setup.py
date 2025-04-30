from setuptools import setup, find_packages

setup(
  name="mucs_database",
  version="0.1.0",
  packages=find_packages(include=["database", "database.*"]),
  install_requires=[
  ],
)