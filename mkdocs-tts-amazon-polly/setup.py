from setuptools import setup, find_packages

setup(
    name="mkdocs-amazon-polly",
    version="0.1",
    packages=find_packages(),
    install_requires=["boto3", "mkdocs"],
    entry_points={
        "mkdocs.plugins": [
            "amazon-polly-tts = mkdocs_amazon_polly.plugin:AmazonPollyTTSPlugin",
        ]
    },
)
