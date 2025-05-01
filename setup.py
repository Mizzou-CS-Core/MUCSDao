from setuptools import setup, find_packages

setup(
  name="mucs_database",
  version="0.5.3.1",
  packages=find_packages(),
  install_requires=[
  "canvas_lms_api @ git+https://github.com/Mizzou-CS-Core/CanvasRequestLibrary.git#egg=canvas_lms_api",
  "peewee",
  ],
)