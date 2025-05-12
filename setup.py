from setuptools import setup, find_packages

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xerus",
    version="0.1.0",
    author="Author Name",
    author_email="author@example.com",
    description="CLI agent built with Huggingface Smolagents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ylankgz/xerus",
    packages=find_packages(),
    install_requires=[
        "smolagents[litellm,toolkit]>=1.15.0",
        "typer>=0.15.3",
        "rich>=14.0.0",
        "python-dotenv>=1.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "xerus=xerus.cli:cli",
        ],
    },
    python_requires=">=3.10",
) 