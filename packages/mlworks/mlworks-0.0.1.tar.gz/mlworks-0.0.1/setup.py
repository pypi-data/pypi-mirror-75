import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlworks", # Replace with your own username
    version="0.0.1",
    author="Adelmo Filho",
    author_email="adelmo.aguiar.filho@gmail.com",
    description="Python Package for Unlimited Machine Learning Works",
    long_description="This package implements several machine learning pipelines as a file",
    long_description_content_type="text/markdown",
    url="https://github.com/adelmofilho/mlworks",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)