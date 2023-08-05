 
from setuptools import setup, find_packages

with open("README.md") as readmeFile:
    readmeStr = readmeFile.read()

setup(
    name="pexpectparser",
    version="0.1.0",
    metadata_version="1.0",
    description="A command line bot library using the pexpect library",
    author="Laurkan Rodriguez",
    author_email="laurkan@engineer.com",
    long_description=readmeStr,
    long_description_content_type="text/markdown",
    url="https://github.com/lorkaan/merge-pipfile.git",
    download_url="https://github.com/lorkaan/pipfilemerge/archive/v0.0.6.tar.gz",
    install_requires =[
        'pexpect',
        'parsegrammar'
    ],
    packages=['pexpectparser'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ]
)