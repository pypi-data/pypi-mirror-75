import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chspi",
    version="1.0.0",
    author="Isaac Fisher",
    author_email="fisheri@carlislestudents.org",
    description="A small set of tools for students in Carlisle High School's Raspberry Pi program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fisheri2004/chspi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "gpiozero",
        "threading"
    ],
    python_requires='>=2.7',
)