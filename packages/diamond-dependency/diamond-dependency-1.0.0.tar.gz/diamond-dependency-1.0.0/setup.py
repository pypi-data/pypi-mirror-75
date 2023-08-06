from setuptools import setup

setup(
    name="diamond-dependency",
    version='1.0.0',
    install_requires=[
        "sub-dependency-a",
        "sub-dependency-b",
    ]
)
