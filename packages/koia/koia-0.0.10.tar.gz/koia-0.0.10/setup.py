import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="koia",  # Replace with your own username
    version="0.0.10",
    author="Kel0",
    author_email="rickeyfsimple@gmail.com",
    description="Sql query builder interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kel0/koia",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
