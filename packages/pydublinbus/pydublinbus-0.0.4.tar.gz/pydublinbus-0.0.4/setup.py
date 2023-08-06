from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pydublinbus",
    version="0.0.4",
    description="Python library to get the real-time transport information (RTPI) for Dublin Bus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="dublin bus RTPI",
    author="Alex Iepuras",
    author_email="iepuras.alex@gmail.com",
    license="MIT",
    url="https://github.com/ialex87/pydublinbus",
    download_url="https://github.com/ialex87/pydublinbus",
    platforms=["any"],
    packages=find_packages(),
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=["requests",],
    tests_requires=["flake8", "pylint", "pytest"],
)
