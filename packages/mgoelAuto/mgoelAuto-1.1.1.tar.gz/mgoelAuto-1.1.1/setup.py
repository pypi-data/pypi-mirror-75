import pathlib
from setuptools import setup, find_packages

# This call to setup() does all the work

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

PACKAGE_NAME = 'mgoelAuto'

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name=PACKAGE_NAME,
    long_description="mgoelAuto Library",
    description='Template python package',
    long_description_content_type="text/markdown",
    version="1.1.1",
    author="Mohit Goel",
    author_email="mohit.goel123@yahoo.co.in",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['mgoelAuto = mgoelAuto.__main__:main']},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=requirements
)