# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:35:46 2020

@author: Gideon Pomeranz

setup.py
"""
import setuptools

def read(path):
    with open(path, 'r') as f:
        return f.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scGP", # Replace with your own username
    version="0.1.5",
    author="Gideon Pomeranz",
    author_email="ucbtpom@ucl.ac.uk",
    description="A package for simple scRNAseq analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gpomeranz/scGP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=read('requirements.txt').strip().split('\n'),
    entry_points={
        'console_scripts': ['scGP=bin.main:main'],
        }
)
