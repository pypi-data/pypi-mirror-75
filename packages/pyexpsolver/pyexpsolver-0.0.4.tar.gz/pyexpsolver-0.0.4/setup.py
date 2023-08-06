import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyexpsolver",
    version="0.0.4",
    author="Alberto Castronovo",
    author_email="alberto.castronovo@hotmail.it",
    description="Automatically solve algebraic expression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/albertocastronovo/pyexpsolver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)