#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from urllib.request import urlopen

def get_requirements():
    send = urlopen('https://raw.githubusercontent.com/ogurechik/mop/master/requirements.txt')
    reqs = [lib.decode('utf8').strip() for lib in send]
    return reqs


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mop-rules",
    version="0.0.1",
    entry_points={
        'console_scripts': ['mop=mop:main'],
    },
    author="Oleg Silver",
    author_email="rav-navini-gego-cutropal@yandex.ru",
    description="Полезная утилита, призванная сделать ваш python проект чище",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ogurechik/mop-rules",
    packages=find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license='MIT',
)
