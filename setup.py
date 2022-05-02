from importlib import import_module
from setuptools import find_packages, setup
from pathlib import Path
from sys import version_info


install_requires = ["luhn", "lxml", "pyyaml", "astroid", "jproperties", "jellyfish", "beautifulsoup4"]
if version_info < (3, 7):  # Python 3.6 requirements
    install_requires.append("dataclasses")

dev_requires = [
    "autoflake~=1.4",
    "autopep8~=1.5",
    "black~=19.10b0",
    "coverage~=4.5",
    "coverage-badge~=1.0",
    "flake8~=3.9",
    "isort~=5.9",
    "pytest~=6.2",
    "pytest-mock~=3.6",
    "pip-tools~=6.2",
    "wheel~=0.37",
    "twine~=3.4",
]


def get_version():
    return import_module("whispers.__version__").__version__


def get_readme():
    return Path(__file__).parent.joinpath("README.md").read_text()


setup(
    name="whispers",
    version=get_version(),
    url="https://github.com/adeptex/whispers",
    author="Artëm Tsvetkov",
    author_email="linkedin@adeptex.net",
    description="Identify secrets in static structured text",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "tests.*")),
    include_package_data=True,
    platforms="any",
    install_requires=install_requires,
    setup_requires=["pytest-runner"],
    tests_require=dev_requires,
    extras_require={"dev": dev_requires},
    entry_points={"console_scripts": ["whispers=whispers.main:cli"]},
)
