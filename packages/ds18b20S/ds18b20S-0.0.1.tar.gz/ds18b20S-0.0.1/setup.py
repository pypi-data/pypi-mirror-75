import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ds18b20S", # Replace with your own username
    version="0.0.1",
    author="Sahak",
    author_email="sahak.sahakyan2017@gmail.com",
    description="A small package for ds18b20S temperature sensor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sahakyansahak/ds18b20S",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
