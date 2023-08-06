import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "expkg-am",
    version = "0.0.2",
    author = "andreamarin",
    author_email = "andrea.marin2411@gmail.com",
    description = "Sample package",
    long_description_content_type="text/markdown",
    long_description = long_description,
    install_requires = [],
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.6"
)
