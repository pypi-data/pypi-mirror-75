import pathlib
from setuptools import setup

# How to use:
# https://packaging.python.org/tutorials/packaging-projects/
# Basically run this command in your python interpreter:
# setup.py sdist bdist_wheel

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="hwglance",
    version="1.0.8",
    description="for Python3 + Console: hwglance; # hwglance: Glance on your computer status # Works on everything running \*NIX, Mac, Windows, anything Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/NamasteJasutin/pywaremon",
    author="NamasteJasutin",
    author_email="justin.duijn@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=["hwglance"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "hwglance=hwglance.__console__:main",
        ]
    },
)