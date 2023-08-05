import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nestily",
    version="0.0.1",
    author="Spencer Bard",
    author_email="sbard26@gmail.com",
    description="Nested ish for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spencerbard/nestily",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
