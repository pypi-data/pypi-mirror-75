import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyinsta3",
    version="1.0",
    author="toxicrecker",
    author_email="reck.channel.mainlead@gmail.com",
    description="pyinsta3 is a package to get instagram profile info of any user.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.google.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=["aiohttp"]
)