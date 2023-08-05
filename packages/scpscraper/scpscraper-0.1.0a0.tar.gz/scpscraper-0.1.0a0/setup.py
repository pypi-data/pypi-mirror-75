from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="scpscraper",
    packages=find_packages(),
    version="0.1.0a0",
    license="MIT",
    author="JaonHax",
    author_email="jaonhax@gmail.com",
    description="A Python library designed for scraping data from the SCP wiki.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JaonHax/scp-scraper",
    keywords=["SCP", "SCP Foundation", "Webscraper", "AI Dataset"],
    install_requires=[
                      "regex",
                      "bs4",
                      "tqdm"
    ],
    classifiers=[
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Development Status :: 3 - Alpha",
                 "Intended Audience :: Developers",
                 "Natural Language :: English",
                 "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ]
)