import setuptools
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

additional_files = ["py.typed"]
for filename in glob.iglob("./faraway/datasets/**", recursive=True):
    if ".csv.bz2" in filename:
        additional_files.append(filename.replace("./faraway/", ""))


setuptools.setup(
    name="faraway",
    version="0.0.6",
    author="Julian Faraway",
    author_email="jjf23@bath.ac.uk",
    description="Datasets and utilities to support books by Julian Faraway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/julianfaraway/LMP",
    packages=setuptools.find_packages(),
    package_data={"faraway": additional_files},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
