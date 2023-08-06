import os
import setuptools


module_dir = os.path.dirname(__file__)
print(module_dir)

# with open("/README.md", "r") as fh:
#     long_description = fh.read()


setuptools.setup(
    name="cloud-control-common",
    version="0.0.6",
    author="Trevor Flanagan",
    author_email="trevor.flanagan@cis.ntt.com",
    description="A Python client for the NTT CloudControl API",
    long_description="long_description",
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
