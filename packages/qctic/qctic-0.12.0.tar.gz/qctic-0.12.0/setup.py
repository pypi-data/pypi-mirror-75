from os import path

import setuptools

from qctic.__version__ import __version__

curr_dir = path.abspath(path.dirname(__file__))

with open(path.join(curr_dir, "README.md")) as fh:
    long_description = fh.read()

setuptools.setup(
    name="qctic",
    version=__version__,
    keywords="quantum simulator qiskit",
    author="Andres Garcia Mangas",
    author_email="andres.garcia@fundacionctic.org",
    description="Qiskit provider to interact with the QCTIC quantum simulator platform",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://bitbucket.org/fundacionctic/erwin-qiskit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License"
    ],
    entry_points={
        "console_scripts": [
            "qcticjob=qctic.cli:main"
        ]
    },
    python_requires=">=3.6",
    install_requires=[
        "qiskit-aer>=0.4.0,<1.0.0",
        "marshmallow>=3.0,<4.0",
        "tornado>=6.0,<7.0"
    ],
    extras_require={
        "dev": [
            "autopep8>=1.5,<2.0",
            "pylint>=2.0,<3.0",
            "rope>=0.16.0,<1.0",
            "pytest>=5.0,<6.0",
            "bumpversion>=0.5.3,<1.0",
            "pytest-httpserver>=0.3.0,<1.0",
            "coloredlogs>=14.0,<15.0",
            "pytest-cov>=2.8.1,<3.0",
            "pytest-asyncio>=0.10.0,<1.0",
            "notebook>=6.0,<7.0",
            "coloredlogs>=14.0,<15.0"
        ],
        "nest": [
            "nest-asyncio>=1.4.0,<2.0"
        ]
    }
)
