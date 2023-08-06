import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="helix-installer", 
    version="0.0.1",
    author=".NET Core Engineering Team",
    author_email="dnceng@microsoft.com",
    description="Placeholder for helix-installer package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/helix-scripts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)