import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fbscrape",
    version="0.0.2",
    author="Edward Marozzi",
    author_email="marozzi.t@gmail.com",
    description="A package to scrape the likes of a facebook page and its posts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ted-marozzi/facebook-likes-scrape",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)