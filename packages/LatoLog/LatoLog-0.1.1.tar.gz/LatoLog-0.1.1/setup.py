import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="LatoLog",
    version="0.1.1",
    author="Fábio Correia",
    description="A package that makes customizing logs easier than expected",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/fabioqcorreia/LatoLog",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "latolog=latolog.main:LatoLog"
        ]
    }
)
