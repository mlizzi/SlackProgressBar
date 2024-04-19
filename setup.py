from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="slack_progress_bar",
    version="2.0.0",
    author="Michael Lizzi",
    author_email="michael.lizzi@hotmail.com",
    description="A Python package for displaying progress bars in Slack messages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mlizzi/slack-progress-bar",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=["slack_sdk"],
)
