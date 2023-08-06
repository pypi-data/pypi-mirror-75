import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="bllog",
    version="1.0.0",
    description="Simple and easy-to-use logger",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/barrow099/bllog",
    author="Barrow099 (Mate Magyar)",
    author_email="mate@barrow099.hu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["bllog"],
    include_package_data=True,
    install_requires=["colorama", "termcolor"],
)
