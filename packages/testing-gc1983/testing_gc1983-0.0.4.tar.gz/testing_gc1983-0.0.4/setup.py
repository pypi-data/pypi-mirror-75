import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testing_gc1983", # Replace with your own username
    version="0.0.4",
    author="Gregory Coyle",
    author_email="gregory.coyle@tufts.edu",
    description="Testing packaging scenarios.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	install_requires=['jupyterlab >= 2.1.5'],
    python_requires='>=3.6'
)