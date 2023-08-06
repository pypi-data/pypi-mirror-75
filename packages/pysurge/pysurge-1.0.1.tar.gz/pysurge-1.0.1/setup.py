from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pysurge",
    use_scm_version=True,
    description=("Write small-scale load tests quickly and easily in python with pysurge"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Brandon Squizzato",
    author_email="bsquizza@redhat.com",
    url="https://www.github.com/bsquizz/pysurge",
    packages=find_packages(),
    keywords=["performance", "load", "testing", "test", "qa"],
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    install_requires=["pyyaml", "click"],
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires=">=3.6",
)
