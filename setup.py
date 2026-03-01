#!/usr/bin/env python
"""
Setup script for BRAINBLUE URBAIN
Allows installation as a package: pip install -e .
"""

from setuptools import setup, find_packages

with open("README_DEPLOYMENT.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="brainblue-urbain",
    version="1.0.0",
    author="BRAINBLUE Team",
    author_email="contact@brainblue.sn",
    description="Advanced GIS Platform for Integrated Urban Water Management in Africa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/BRAINBLUE",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.1",
            "flake8>=6.0.0",
            "pylint>=2.17.5",
        ],
        "ml": [
            "tensorflow>=2.13.0",
            "keras>=2.13.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "brainblue=backend.app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
