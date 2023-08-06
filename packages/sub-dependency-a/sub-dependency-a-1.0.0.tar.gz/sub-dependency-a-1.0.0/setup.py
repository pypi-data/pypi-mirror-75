from setuptools import setup

setup(
    name="sub-dependency-a",
    version='1.0.0',
    install_requires=[
        "sub-dependency-d<1.0.0",
    ]
)
