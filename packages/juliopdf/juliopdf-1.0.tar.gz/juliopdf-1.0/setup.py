import setuptools
from pathlib import Path


setuptools.setup(
    name="juliopdf",
    version=1.0,
    long_descreption=Path("README.md").read_text(),
    packages=setuptools.find_namespace_packages(exclude=["test", "data"])
)
