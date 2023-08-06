from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="thonny-struktog-test",
    version="0.0.2",
    author="niklaskeerl",
    author_email="niklas.keerl@mailbox.org",
    description="Struktog webdriver client plugin for thonny",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DDI-TU-Dresden/thonny-webdriver/tree/struktog",
    install_requires=requirements,
    packages=["thonnycontrib.struktog"],
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Software Development",
    ],
    python_requires=">=3.5",
)
