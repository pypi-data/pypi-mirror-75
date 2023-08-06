import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datup",
    version="0.1.8_6",
    author="Datup DevOps",
    author_email="devops@datup.ai",
    description="The version of this library and document is V 0.1.8_6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://datup.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["boto3","statsmodels==0.11.0","s3fs","scipy","sklearn"],
    python_requires='>=3.6'
)
