import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="balance-sheet",
    version="0.2.0",
    description="A personal balance sheet program",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/evanaze/balance-sheet",
    author="Evan Azevedo",
    author_email="evanazzvd@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=False,
    entry_points={
        "console_scripts": [
            "realpython=src.__main__:main",
        ]
    },
)