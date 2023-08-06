"""
NeurodataLab LLC 19.07.2019
Created by Andrey Belyaev
"""
import setuptools
import sys

try:
    library_version = "1.1.6a1"
except KeyError:
    sys.exit("You need to set library version into NDL_LIBRARY_VERSION variable")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ndl-api",
    version=library_version,
    author="Neurodata Lab",
    author_email="admin@neurodatalab.dev",
    description="Neurodata Lab API tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'grpcio>=1.22',
        'grpcio-tools>=1.22',
        'protobuf>=3.9.0',
        'opencv-python>=4.1.0.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
