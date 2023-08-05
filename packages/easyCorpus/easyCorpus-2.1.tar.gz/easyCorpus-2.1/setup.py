import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyCorpus",
    version="2.1",
    author="Sheng Lu, Sanjun Sun",
    author_email="lus@brandeis.edu",
    description="a simple corpus tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boblus/easyCorpus",
    packages=['easyCorpus'],
    install_requires=[
        'jieba',
        'matplotlib',
        'nltk',
        'numpy',
        'pandas',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.7',
)
