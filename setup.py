# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="vatu",
    version="0.0.1",
    author="Benjamin Maisonnas",
    author_email="ben@wainei.net",
    description="Tool to record and fine-tune power and clocks on AMD Radeon RX Vega cards",
    long_description=readme,
    license="GPLv3",
    keywords="gpu",
    url="https://github.com/benzhaomin/vatu",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],

    packages=find_packages(exclude=("tests", "docs")),
    package_data={
        "vatu": [],
    },
    test_suite="tests",
    entry_points={
        "console_scripts": ["vatu = vatu.cli:main"],
    },
    install_requires=[],
    extras_require={
        "dev": ["nose", "flake8"],
    },
)
