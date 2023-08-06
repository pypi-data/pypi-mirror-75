import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="sharkiqpy",
    version="0.1.4",
    description="Python API for Shark IQ robots",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ajmarks/sharkiq",
    author="Andrew Marks",
    author_email="ajmarks@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["sharkiqpy"],
    include_package_data=False,
    install_requires=["aiohttp", "requests"],
)
