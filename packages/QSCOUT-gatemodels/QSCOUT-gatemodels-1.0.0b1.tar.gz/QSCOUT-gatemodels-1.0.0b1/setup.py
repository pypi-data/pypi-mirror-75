"""QSCOUT Gate Models"""

import sys
from setuptools import setup, find_packages

name = "QSCOUT-gatemodels"
description = "QSCOUT Gate Models"
version = "1.0.0b1"

setup(
    name=name,
    description=description,
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    version=version,
    author="Benjamin C. A. Morrison, Jay Wesley Van Der Wall, Daniel Lobser, Antonio Russo, Kenneth Rudinger, Peter Maunz",
    author_email="qscout@sandia.gov",
    packages=find_packages(include=["qscout", "qscout.*"]),
    package_dir={"": "."},
    install_requires=["JaqalPaq", "numpy"],
    extras_require={"tests": ["pytest"],},
    python_requires=">=3.6",
    platforms=["any"],
    url="https://qscout.sandia.gov",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
    ],
)
