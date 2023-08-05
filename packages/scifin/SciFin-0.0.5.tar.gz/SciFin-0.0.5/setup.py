import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SciFin",
    version="0.0.5",
    author="Fabien Nugier",
    author_email="fabien.nugier@outlook.com",
    description="SciFin is a python package for Science and Finance.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SciFin-Team/SciFin",
    packages=setuptools.find_packages(include=['scifin', 'scifin.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['numpy>=1.18.1',
    'pandas>=1.0.3',
    'datetime',
    'bs4>=4.8.2',
    'requests>=2.23.0',
    'pandas_datareader>=0.8.1',
    'IPython>=7.13.0',
    'scipy>=1.4.1',
    'statsmodels>=0.11.0',
    'sklearn>=0.22.1',
    'matplotlib>=3.1.3'],
)

