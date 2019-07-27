import setuptools

with open("README_PyPI.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-minesweeper",
    version="0.1.1",
    author="Baibhav Vatsa",
    description="Minesweeper module for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BaibhaVatsa/minesweeper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)