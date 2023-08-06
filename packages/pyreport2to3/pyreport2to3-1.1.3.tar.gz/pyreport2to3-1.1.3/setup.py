import os.path

from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="pyreport2to3",
    version="1.1.3",
    author="Maurya Allimuthu",
    author_email="catchmaurya@gmail.com",
    description="Python 2 to 3 porting HTML report ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/catchmaurya/pyreport2to3",
    packages=find_packages(),
    #scripts=['df_style.css',],
    data_files=[('/', ['pyreport2to3/df_style.css'])],
    install_requires=['2to3>=1.0','future>=0.18.2', 'Jinja2>=2.11.2', 'matplotlib>=2.2.5','modernize>=0.7', 'numpy>=0.7', 'pandas>=0.24.2'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
