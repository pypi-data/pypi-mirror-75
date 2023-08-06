

import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xiaomeilv",
    version="0.0.1",
    author="xiaomeilv",
    author_email="jiajieyuan666@gmail.com",
    description="just a test demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiajieyuan1010/kaggle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)    