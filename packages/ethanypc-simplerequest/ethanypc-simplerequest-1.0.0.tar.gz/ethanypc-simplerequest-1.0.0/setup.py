from setuptools import setup

with open("README.md", 'r') as fid:
    README = fid.read()

setup(
    name="ethanypc-simplerequest",
    version="1.0.0",
    description="Wrapper around http.client",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Ethan",
    author_email="ypcethan@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["simplehttp"],
)
