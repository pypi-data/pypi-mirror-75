import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zk-cli",
    version="0.0.2",
    author="Tom Firth",
    description="A command lind utility for Zettelkasten",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tdfirth/zk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["zk=zk.zk:main"]},
    extras_require={
        "dev": ["nose"]
    }
)
