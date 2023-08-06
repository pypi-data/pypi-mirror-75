import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cazact", # Replace with your own username
    version="0.0.0",
    author="Gene Dan",
    author_email="genedan@gmail.com",
    description="Property and Casualty Loss Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/genedan/cazact",
    project_urls={
        "Documentation": "https://genedan.com/cazact/docs"
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6.0',
)
