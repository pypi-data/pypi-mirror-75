import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="a_parser",
    version="2.0.1",
    author="A-Parser",
    author_email="support@a-parser.com",
    description="A-Parser API Module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a-parser/api-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='==2.7.*',
)
