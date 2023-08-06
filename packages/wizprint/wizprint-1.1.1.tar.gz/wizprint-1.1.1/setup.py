import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="wizprint",
    version="1.1.1",
    description="for Python3 + Console: wprint; A Small Gimmick that makes printing tasks to console just a bit more fun by introducing a Wizard that will tell you your customized message in a bubble. | fnt; Adds Console Coloring and Emojis for wprint.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/NamasteJasutin/wizprint",
    author="NamasteJasutin",
    author_email="justin.duijn@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=["wizprint"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "wprint=wizprint.console:main",
        ]
    },
)