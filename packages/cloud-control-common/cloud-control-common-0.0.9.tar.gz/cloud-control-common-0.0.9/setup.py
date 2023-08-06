import os
import setuptools


setuptools.setup(
    name="cloud-control-common",
    version="0.0.9",
    author="Trevor Flanagan",
    author_email="trevor.flanagan@cis.ntt.com",
    description="A Python client for the NTT CloudControl API",
    long_description="This is a simple python library for interacting with NTT Cloud Control API (version 2.13).",
    packages=setuptools.find_packages(),
    package_data={
        "tests": ["json/*.json"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
