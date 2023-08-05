from setuptools import setup, find_packages

with open("README.md") as readmeFile:
    readmeStr = readmeFile.read()

setup(
    name="parsegrammar",
    version="0.1.0",
    metadata_version="1.0",
    description="A library with Symbol Graph and Grammar classes",
    author="Laurkan Rodriguez",
    author_email="laurkan@engineer.com",
    long_description=readmeStr,
    long_description_content_type="text/markdown",
    url="https://github.com/lorkaan/parsegrammar.git",
    download_url="https://github.com/lorkaan/parsegrammar/archive/v0.1.0.tar.gz",
    install_requires =[],
    packages=['parsegrammar'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ]
)
