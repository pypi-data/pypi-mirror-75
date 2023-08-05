import os

from setuptools import find_packages
from setuptools import setup

with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8",
) as f:
    long_description = f.read()

setup(
    name="lung",
    version="0.1.4",
    author="MinRegret",
    author_email="minregret@minimizingregret.com",
    url="https://github.com/MinRegret/Ventilator-Dev",
    description="Lung simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["numpy", "pandas", "h5py"],
    extras_require={"dev": ["timecast", "bumpversion", "pre-commit", "ipython", "jupyter"]},
    packages=find_packages(),
)
