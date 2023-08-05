import setuptools


with open("README.md", "r") as rfh:
    long_description = rfh.read()


setuptools.setup(
    name = "keyprotect",
    version = "2.0.0",
    description = "A Pythonic client for IBM Key Protect",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/IBM/keyprotect-python-client",
    license = "Apache 2.0",
    author = "Mathew Odden",
    author_email = "mathewrodden@gmail.com",
    packages = setuptools.find_packages(),
    install_requires = [
        "redstone==0.3.0",
    ],
    python_requires=">=3.5",
    classifiers = [
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
)
