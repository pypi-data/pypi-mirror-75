import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BioGraph",
    version="0.0.1",
    author="Soo Heon Kim",
    author_email="sooheon.k@gmail.com",
    description="Molecular graphs and the neural networks to embed them.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sooheon/BioGraph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    python_requires='>=3.6',
)
