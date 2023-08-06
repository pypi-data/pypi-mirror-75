from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='brule',
    version='0.2.0',
    author="Davis Busteed",
    author_email="busteed.davis@gmail.com",
    license="MIT",
    description="Dr. Steve Brule name generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbusteed/brule",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)