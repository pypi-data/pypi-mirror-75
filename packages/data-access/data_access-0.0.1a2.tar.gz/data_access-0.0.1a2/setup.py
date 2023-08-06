import os

import setuptools


def select_all_folders(root):
    if root is None:
        raise TypeError("root folder can't be None")

    return [x[0] for x in os.walk(root)]


with open("README.md", "r") as fh:
    long_description = fh.read()

folders = [select_all_folders("data_access")]

setuptools.setup(
    name="data_access",
    version="0.0.1-alpha.2",
    author="almdudleer",
    author_email="leshaserdyukov@gmail.com",
    description="A library for easy multi-source data access",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LearningAnalyticsITMO/data-access",
    download_url="https://github.com/LearningAnalyticsITMO/data_access/archive/v0.0.1-alpha.2.tar.gz",
    packages=[y for x in folders for y in x],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.6",
)
