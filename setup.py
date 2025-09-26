from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="jsieve",
    version="0.1.0",
    author="M. Murat Ardag",
    author_email="",  
    description="JavaScript Extractor & Enumerator for web security analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mmuratardag/JSieve",
    project_urls={
        "Bug Tracker": "https://github.com/mmuratardag/JSieve/issues",
        "Documentation": "https://mmuratardag.github.io/JSieve",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "jsieve=jsieve.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["wordlists/*.txt"],
    },
    keywords="javascript, web security, enumeration, reconnaissance, bug bounty, penetration testing",
)