#!/bin/env python3
from setuptools import setup, find_packages

setup(
  name="psearcherr", version="0.1.1",
  url="https://github.com/duangsuse-valid-projects/psearcher-r",
  author="duangsuse", author_email="fedora-opensuse@outlook.com", license="MIT",
  description="Rewrite for Python baidu search client: iridesc/psearcher",
  long_description=open("README.md").read(), long_description_content_type="text/markdown",
  packages=find_packages(),
  install_requires=["requests>=2.0.0", "retry>=0.8.0", "bs4>=0.0.1", "loger>=0.1.0"],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)