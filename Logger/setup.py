"""
Setup script for the Logger library.
This is optional - the library can be used by simply copying the Logger folder.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="portable-logger",
    version="1.0.0",
    author="Logger Library",
    description="A portable, self-contained logging library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Logging",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No external dependencies required!
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ],
        "optional": [
            "colorama",  # For better color support on Windows
            "rich",      # For rich text formatting
        ],
    },
    entry_points={
        "console_scripts": [
            "logger-demo=Logger.demo:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 