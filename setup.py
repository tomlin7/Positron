"""
Positron - Electron-like framework for Python + React
"""

from pathlib import Path

from setuptools import find_packages, setup

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = (
    readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""
)

setup(
    name="positron-native",
    version="0.1.0",
    author="Positron Contributors",
    description="Build cross-platform desktop apps with React and Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomlin7/positron",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pywebview>=6.1.0",
        "pythonnet>=3.0.5",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
