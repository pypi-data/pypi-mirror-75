import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oxlate",
    version="0.0.1",
    author="JP Slavinsky",
    author_email="jps@rice.edu",
    description="OpenStax Lambda@Edge utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openstax/late-python",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
