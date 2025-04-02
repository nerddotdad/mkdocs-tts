from setuptools import setup, find_packages

setup(
    name="mkdocs-tts-amazon-polly",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mkdocs>=1.0",
        "boto3",
    ],
    entry_points={
        "mkdocs.plugins": [
            "tts-amazon-polly = mkdocs_tts_amazon_polly.plugin:AmazonPollyTTSPlugin",
        ]
    },
    include_package_data=True,
    description="An MkDocs plugin to generate TTS audio using Amazon Polly",
    author="TJ Hoth",
    author_email="itzteajay@gmail.com",
    url="https://github.com/nerddotdad/mkdocs-tts-amazon-polly",
    classifiers=[
        "Framework :: MkDocs",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
