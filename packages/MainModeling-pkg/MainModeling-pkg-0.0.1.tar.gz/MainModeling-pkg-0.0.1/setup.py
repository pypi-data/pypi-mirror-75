import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MainModeling-pkg",
    version="0.0.1",
    author="Edgar David Mora Martinez",
    author_email="edgar.mora@diseniosm.com",
    description="Structural Analysis and Soft Computing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://http://www.diseniosm.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
)