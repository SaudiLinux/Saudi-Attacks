#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="saudi-attacks",
    version="1.1.0",
    author="Saudi Linux",
    author_email="SaudiLinux7@gmail.com",
    description="أداة شاملة للاختبار الأمني واكتشاف الثغرات",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SaudiLinux/Saudi-Attacks",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Security",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Natural Language :: Arabic",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "saudi-attacks=saudi_attacks:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)