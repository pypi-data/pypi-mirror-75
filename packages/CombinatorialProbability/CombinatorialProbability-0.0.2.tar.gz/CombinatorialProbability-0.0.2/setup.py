import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="CombinatorialProbability", # Replace with your own username
    version="0.0.2",
    author="Stephen DeSalvo",
    author_email="stephendesalvo@gmail.com",
    description="A POC for a combinatorial probability library using integer partitions as one example",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/combinatorialprobability",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
)