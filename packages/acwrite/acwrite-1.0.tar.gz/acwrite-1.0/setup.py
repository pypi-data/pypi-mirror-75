from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()

install_requires = []
with open("requirements.txt","r") as f:
    line = f.readline()
    while line:
        install_requires.append(line.rstrip())
        line = f.readline()

setup(
    name= "acwrite",
    version = "1.0",
    author="Yi Yu",
    author_email="q1499114179@gmail.com",
    description="A python package for writing academic papers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yoki0/acwriting",
    packages = find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_requires,
    scripts=['bin/acword']
    )
