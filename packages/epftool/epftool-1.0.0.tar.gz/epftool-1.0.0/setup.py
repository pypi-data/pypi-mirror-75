from setuptools import setup
from epftool.cli import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="epftool",
    version=__version__,
    author="Illidan",
    description="Command line tool to search EPF files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Illidanz/epftool",
    packages=["epftool"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["epftool=epftool.cli:main"],
    },
    install_requires=[
        "click>=7.1",
        "tqdm>=4.48"
    ],
    python_requires=">=3.7",
)
