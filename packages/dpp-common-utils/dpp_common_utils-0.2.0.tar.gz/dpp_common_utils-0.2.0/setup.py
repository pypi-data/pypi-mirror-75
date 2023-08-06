import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('VERSION') as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name="dpp_common_utils",
    version=version,
    author="J. Hohenstein",
    author_email="j.hoh@t-online.de",
    description="A small utils package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.uni-due.de/",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=[
        'selenium~=3.141.0',
        'chromedriver-binary~=83.0.4103.39.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)