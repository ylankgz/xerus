from setuptools import setup, find_packages

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xerus-ai",
    version="0.0.6",
    author="Ulan Abdurazakov",
    author_email="ylankgz@gmail.com",
    description="CLI agent for training and finetuning ML models, built with Huggingface Smolagents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ylankgz/xerus",
    packages=find_packages(),
    package_data={
        'xerus': ['config_template.toml'],
    },
    include_package_data=True,
    install_requires=[
        "smolagents[litellm,toolkit]>=1.15.0",
        "rich-click>=1.8.8",
        "python-dotenv>=1.1.0",
        "toml>=0.10.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "xerus=xerus.cli:main",
        ],
    },
    python_requires=">=3.10",
) 