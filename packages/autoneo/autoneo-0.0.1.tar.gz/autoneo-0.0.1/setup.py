import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoneo",
    version="0.0.1",
    author="Raghavprasanna Rajagopalan",
    author_email="raghavp96@gmail.com",
    description="A simple tool for building graph databases from multiple relational sources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raghavp96/autoneo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "neo4j>=4.1.0"
    ]
)
