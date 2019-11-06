import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wnbAPI",
    version="0.0.1",
    author="Devin Nicholas Arnold",
    author_email="devinnarnold@gmail.com",
    description="Toolkit for accessing WNBA stats API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ahimsaka/wnbAPI-Tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)