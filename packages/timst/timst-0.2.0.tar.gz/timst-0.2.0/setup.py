"""
This file contains the current state of packaging in Python using
Distribution Utilities (Distutils) and its extension from the end
user'point-of-view.

Documentation:
https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/introduction.html
"""

import os
import re
import sys
from setuptools import setup
from setuptools import find_packages

PACKAGE = "timst"

# Used for pytest and code coverage
TESTS_REQUIEREMENTS = ["pytest", "pytest-cov"]
# Depending on the documents more dependencies can be added
DOCS_REQUIEREMENTS = ["recommonmark", "sphinx_rtd_theme", "sphinxcontrib-bibtex"]
# Dependencies for the packages
PACKAGE_REQUIEREMENTS = ["numpy", "torch", "tqdm", "torchvision"]

# Check python version
if sys.version_info < (3, 6):
    print(f"{PACKAGE} requires Python 3.6 or later", file=sys.stderr)
    sys.exit(1)

# Read through Readme
try:
    this_directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except IOError:
    print("Read me file not found.")


def get_version():
    """Gets the version from the package's __init__ file
    if there is some problem, this fails.
    """
    VERSIONFILE = os.path.join("src", PACKAGE, "__init__.py")
    initfile_lines = open(VERSIONFILE, "rt").readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)


setup(
    name=PACKAGE,
    version=get_version(),
    description="Image style transfer using Torch",
    long_description=long_description,
    author="Tanjona R. Rabemananjara",
    author_email="tanjona.rabemananjara@mi.infn.it",
    url="https://github.com/Radonirinaunimi/Style-Transfer",
    install_requires=PACKAGE_REQUIEREMENTS,
    extras_require={"docs": DOCS_REQUIEREMENTS, "tests": TESTS_REQUIEREMENTS},
    entry_points={"console_scripts": ["timst = timst.run:main", ]},
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    classifiers=[
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
