import pathlib
from setuptools import setup, find_packages

# This call to setup() does all the work

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

PACKAGE_NAME = 'pneuro'

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name=PACKAGE_NAME,
    long_description="pneuro Library",
    description='Template python package',
    long_description_content_type="text/markdown",
    version="1.2.9",
    #version="1.2.5", #Most Stable Version
    author="Punit Nanda",
    author_email="punit.nanda01@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['pneuro = pneuro.__main__:main']},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=requirements
)