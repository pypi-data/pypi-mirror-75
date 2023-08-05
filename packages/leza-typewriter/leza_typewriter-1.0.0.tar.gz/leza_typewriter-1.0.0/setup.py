import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# short description
desc = "function for printing text in a type writer manner"

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="leza_typewriter",
    version="1.0.0",
    description=desc,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ElLoko233/typwriter",
    author="Lelethu Futshane",
    classifiers=["License :: OSI Approved :: MIT License", "Programming Language :: Python :: 3", "Programming Language :: Python :: 3.8"],
    packages=["typewriter"],
    include_package_data=True,
)
