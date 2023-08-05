import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simpleprotocol", # Replace with your own username
    version="1.0.1",
    author="Ben Hack",
    author_email="benjamin.hack@balliol.ox.ac.uk",
    description="A package for using a basic protocol socket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chinbob2515/python-simpleprotocol",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
