import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrandorg",
    version="1.0.1",
    author="Alberto Castronovo",
    author_email="alberto.castronovo@hotmail.it",
    description="Request numbers from random.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/albertocastronovo/pyrandorg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)