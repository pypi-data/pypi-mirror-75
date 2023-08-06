from setuptools import setup

with open("./README.md", "r") as f:
    l_desc = f.read()

setup(
    name="ascify",
    version="1.0",
    author="theonekeyg",
    author_email="theonekeyg@gmail.com",
    description="Lightweight library for turning images to grid of ascii tokens",
    long_description=l_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/theonekeyg/ascify",
    packages=["ascify",],
    install_requires=[
        "numpy>=1.13.0",
        "Pillow>=6.0"
    ]
)
