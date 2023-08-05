import pathlib
import re
import sys

from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
PACKAGE_NAME = "hal9k_api"

CONST_TEXT = (HERE / f"{PACKAGE_NAME}/const.py").read_text()
VERSION = re.search('__version__ = "([^\']+)"', CONST_TEXT).group(1)

setup(
    name="Hal9k-API",
    version=VERSION,
    description="The HackerLab 9000 API Server.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="hacker hacking lab laboratory virtual machine virtualbox vm flask",
    url="https://github.com/haxys-labs/Hal9k-Overmind-API",
    project_urls={
        "Source Code": "https://github.com/haxys-labs/Hal9k-Overmind-API",
        "Documentation": "https://github.com/haxys-labs/Hal9k-Overmind-API",
    },
    author="CMSteffen",
    author_email="cmsteffen@haxys.net",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
        "Topic :: Security",
        "Topic :: System",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    packages=[PACKAGE_NAME],
    include_package_data=True,
    install_requires=[
        "Lib-Hal9k >=0.7.0", "flask >=1.1.2", "flask-cors >=3.0.8"
    ],
    entry_points={},
)
