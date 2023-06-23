import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KMLPlus",  # Replace with your own username
    version="3.0.0-beta.6",
    author="Mark Henderson",
    author_email="mark.henderson1988@gmail.com",
    description="A Python library for creating 3d floating polygons and circles in .kml for Google Earth.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MHenderson1988/kmlplus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
