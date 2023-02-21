from importlib import import_module
from setuptools import find_packages, setup
from pathlib import Path
from sys import version_info


install_requires = [
    "astroid",
    "beautifulsoup4",
    "crossplane",
    "jellyfish",
    "jproperties",
    "luhn",
    "lxml",
    "pyyaml",
]

# Python 3.6 requirements
if version_info < (3, 7):
    install_requires += ["dataclasses"]

dev_requires = [
    "autoflake~=1.4",
    "autopep8~=1.5",
    "black~=22.6",
    "build~=0.8",
    "coverage~=6.4",
    "coverage-badge~=1.0",
    "flake8~=3.9",
    "isort~=5.9",
    "pytest~=7.1",
    "pytest-mock~=3.6",
    "pip-tools~=6.2",
    "wheel~=0.37",
    "twine~=3.4",
]


def get_readme():
    return Path(__file__).parent.joinpath("README.md").read_text()


setup(
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "tests.*")),
    include_package_data=True,
    platforms="any",
    install_requires=install_requires,
    setup_requires=["pytest-runner"],
    tests_require=dev_requires,
    extras_require={"dev": dev_requires},
)
