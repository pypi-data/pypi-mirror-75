# Based on example by Kenneth Reitz
# (https://github.com/navdeep-G/samplemod/blob/master/setup.py)

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="deduce_uces",
    version="1.0.0",
    description="A tool for finding ultraconserved elements across multiple genomes",
    long_description=readme,
    author="UNSW BINF6111 Team UCE",
    url="https://gitlab.cse.unsw.edu.au/z5165557/deduce",
    packages=find_packages(exclude=("tests", "docs")),
    # From https://medium.com/@trstringer/the-easy-and-nice-way-to-do-cli-apps-in-python-5d9964dc950d
    entry_points={"console_scripts": ["deduce = deduce.__main__:main"]},
    install_requires=["mappy", "tqdm", "gffutils", "networkx"],
)
