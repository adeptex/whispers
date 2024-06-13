from importlib import import_module
from pathlib import Path

from setuptools import find_packages, setup

VERSION = import_module("whispers.__version__").__version__


def res(filename: str) -> str:
    """Read package resource"""
    return Path(__file__).parent.joinpath(filename).read_text()


install_requires = res("requirements.txt").split("\n")
dev_requires = res("requirements-dev.txt").split("\n")
readme = res("README.md")

setup(
    name="whispers",
    version=VERSION,
    url="https://github.com/adeptex/whispers",
    author="Artëm Tsvetkov",
    author_email="adeptex@users.noreply.github.com",
    description="Identify secrets in static structured text",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "tests.*")),
    include_package_data=True,
    platforms="any",
    install_requires=install_requires,
    setup_requires=["pytest-runner"],
    tests_require=dev_requires,
    extras_require={"dev": dev_requires},
    entry_points={"console_scripts": ["whispers=whispers.main:main"]},
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)
