import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amirkabirtsa", 
    version="0.0.4",
    author="Masoud Ghasemi",
    author_email="masoud.aut.ac@gmail.com",
    description="TSA Students Projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url ="https://RacinSoft@dev.azure.com/RacinSoft/TSALibraries/_git/TSALibraries",
    download_url ="https://RacinSoft@dev.azure.com/RacinSoft/TSALibraries/_git/TSALibraries",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)