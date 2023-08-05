import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tols",
    version="0.1",
    author="HongRui Chen. SNBCK",
    author_email="snbckcode@gmail.com",
    description="TOLS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snbck/tols",
    packages=setuptools.find_packages(),
)