import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mgoelAuto", # Replace with your own username
    version="0.0.8",
    author="mgoelAuto",
    author_email="mohit.goel123@yahoo.co.in",
    description="Automatic deploy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/EmployeeSurveillanceFileTransfer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
