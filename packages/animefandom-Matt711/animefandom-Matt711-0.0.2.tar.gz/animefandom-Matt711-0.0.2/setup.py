import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="animefandom-Matt711", # Replace with your own username
    version="0.0.2",
    author="Matthew Murray",
    author_email="matthewmurray711@gmail.com",
    description="Simple web scraper for fandom anime summaries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Matt711/animefandom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)