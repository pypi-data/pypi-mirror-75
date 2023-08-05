import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qq_training_wheels", # Replace with your own username
    version="0.0.1",
    author="Shashank Yadav",
    author_email="shashank@auquan.com",
    description="Getting started with some basic functionalities of Quant Quest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/qq_training_wheels",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)