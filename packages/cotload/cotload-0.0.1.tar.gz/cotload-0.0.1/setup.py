import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cotload",
    version="0.0.1",
    author="Aryan Thakur",
    author_email="aryan.aparna.thakur@gmail.com",
    description="Cotload CORE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        
    ],
    python_requires='>=3.7',
)