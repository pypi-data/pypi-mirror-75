import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uclacatalog",
    version="1.0.0",
    author="Nicholas Nhien",
    author_email="nknhien@ucla.edu",
    description="A Python library to retrieve course and section information from the UCLA Registrar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nnhien/uclacatalog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search"
    ],
    install_requires=['beautifulsoup', 'lxml', 'requests'],
    python_requires='>=3.6',
)