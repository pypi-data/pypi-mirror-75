import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="singleton-firebase",
    version="0.0.2",
    author="Moisés Rangel",
    author_email="moises.rangel@gmail.com",
    description="A Singleton factory to firebase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/cargamos/firebase",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)