import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RavenStyleMatrixProblems",
    version="0.1.0",
    author="Can Serif Mekik",
    author_email="can.mekik@gmail.com",
    description="Create problems in the style of Raven's Matrices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cmekik/pyClarion",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    python_requires='>=3.7',
    install_requires=[
            'pycairo',
        ]
)