from setuptools import setup, find_packages
import django_nacos as nacos


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="django_nacos",
    version=nacos.__version__,
    packages=find_packages(exclude=["test"]),
    url="https://github.com/nacos-group/nacos-sdk-python",
    license="Apache License 2.0",
    author="nacos",
    author_email="755063194@qq.com",
    description="Python client for Nacos.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
)
