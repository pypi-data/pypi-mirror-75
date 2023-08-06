import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Songhan1008",
    version="0.0.1",
    author="Songhan",
    author_email="songhan@yeah.net",
    description="An example for PY84 Courses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/somebody/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)