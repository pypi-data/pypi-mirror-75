# coding=utf-8
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="example-pkg-Tanyee",
  version="0.0.1",
  author="Tanyee Zhang",
  author_email="author@example.com",
  description="An example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/TanyeeZhang/my-python-demo",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
