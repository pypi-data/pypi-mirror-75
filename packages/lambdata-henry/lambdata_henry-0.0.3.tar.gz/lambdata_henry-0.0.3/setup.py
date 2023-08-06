"""
lambdata - collection of helper function, a part of Unit-3 assignment
"""

import setuptools

REQUIRED = [
    "numpy",
    "pandas"
]

with open("README.md", "r") as file:
    long_description = file.read()


setuptools.setup(
    name="lambdata_henry", 
    version="0.0.3",
    author="Henry Gultom",
    author_email="henryspg@gmail.com",
    description="date_extract, state-abbreviation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henryspg/lambdata",
    packages=setuptools.find_packages(),
    install_requires=REQUIRED,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)