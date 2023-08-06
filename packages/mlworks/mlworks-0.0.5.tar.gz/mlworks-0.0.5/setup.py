#!/usr/bin/env python
"""mlworks distutils configuration."""
from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'numpy',
    'pandas'
]

setup(
    name="mlworks",
    version="0.0.5",
    author="Adelmo Filho",
    author_email="adelmo.aguiar.filho@gmail.com",
    description="Python Package for Unlimited Machine Learning Works",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adelmofilho/mlworks",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Natural Language :: Portuguese (Brazilian)",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    keywords=[
        "mlworks",
        "Python",
        "projects",
        "machine-learning",
        "feature-engineering",
        "modelling",
        "data-science"
    ],
    python_requires='>=3.6',
)