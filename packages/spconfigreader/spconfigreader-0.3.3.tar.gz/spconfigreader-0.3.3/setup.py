import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='spconfigreader',
    version='0.3.3',
    author="Moritz Momper",
    author_email="moritz.momper@gmail.com",
    description="A utitlity to read config from yaml-files and environment (like Spring for Java)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Momper14/configreader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ], install_requires=[
        'confuse>=1.0.0',
    ],
    python_requires='>=3.6',
)
