import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dataset-generator",
    version="0.0.1",
    author="Akash Kumar . S",
    author_email="akasharul2101@gmail.com",
    description="A package for generating Image datasets given some backgrounds and objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shiny-Akash/dg.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)