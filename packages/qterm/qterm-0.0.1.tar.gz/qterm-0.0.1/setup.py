import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qterm",
    version="0.0.1",
    author="SH21",
    author_email="anosovigor404@gmail.com",
    description=("QTerm is a Python module for spawning child "
                 "applications and controlling them automatically"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SH659/QTerm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)
