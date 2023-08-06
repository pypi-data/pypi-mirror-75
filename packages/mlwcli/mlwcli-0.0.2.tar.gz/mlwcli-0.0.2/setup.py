#!/usr/bin/env python
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'click'
]

setup(
    name='mlwcli',
    version='0.0.2',
    description='Command Line Interface for mlworks python package',
    long_description=long_description,
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
                "Topic :: Scientific/Engineering :: Artificial Intelligence"],
    keywords=[
            "mlworks",
            "Python",
            "projects",
            "machine-learning",
            "feature-engineering",
            "modelling",
            "data-science"],
    url='https://github.com/adelmofilho/mlw-cli',
    author="Adelmo Filho",
    author_email="adelmo.aguiar.filho@gmail.com",
    license='MIT',
    dependencies=['click'],
    packages=['mlwcli'],
    entry_points={
        'console_scripts': [
            'mlw=mlwcli.mlwcli:mlwcli'
        ]
    })
