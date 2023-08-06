import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ogdp_apis",
    version="0.1",
    author="Ayush Shenoy",
    author_email="masala_man@protonmail.com",
    description="A python wrapper for data.gov.in APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/masala-man/ogdp-apis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
