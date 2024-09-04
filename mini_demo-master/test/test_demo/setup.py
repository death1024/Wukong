#!/usr/bin/env python3
# coding=utf-8

import setuptools

setuptools.setup(
    name="test_demo",
    version="1.0.0",
    author='wyx',
    author_email='jingjing.deng@ubtrobot.com',
    description="demo with mini_sdk",
    long_description='demo with mini_sdk,xxxxxxx',
    long_description_content_type="text/markdown",
    license="GPLv3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'alphamini > 0.1.3',
    ],
    entry_points={
        'console_scripts': [
            'test_demo = play_test.test:main'
        ],
    },
    zip_safe=False
)
