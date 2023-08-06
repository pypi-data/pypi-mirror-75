from setuptools import setup

import sirex  # method #6 in https://packaging.python.org/guides/single-sourcing-package-version/ for getting the package attributes

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="sirex",
    version=sirex.__version__,  # from the init file
    summary = sirex.__summary__,
    title=sirex.__title__,
    description="Simple Regex - A package to use regex commands on strings using simple function calls",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url=sirex.__uri__,
    author=sirex.__author__,
    author_email=sirex.__email__,
    license=sirex.__license__,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["sirex"],
    include_package_data=True,
)


