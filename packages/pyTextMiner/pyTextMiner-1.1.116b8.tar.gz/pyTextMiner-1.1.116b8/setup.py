import setuptools
from pyTextMiner import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyTextMiner", # Replace with your own username
    version=__version__,
    author="Min Song",
    author_email="min.song@yonsei.ac.kr",
    description="A text mining tool for Korean and English",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MinSong2/pyTextMiner",
    packages=setuptools.find_packages(exclude = []),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "cython",
        "kobert-transformers",
        "transformers==2.9.1",
        "sklearn-crfsuite",
        "pytorch-pretrained-bert",
        "gensim==3.8.1",
        "konlpy==0.5.1",
        "krwordrank==1.0.2",
        "kss==1.3.1",
        "lxml==4.5.0",
        "matplotlib==3.2.1",
        "mecab-python3",
        "networkx==2.2",
        "nltk==3.4.5",
        "node2vec",
        "bs4",
        "numpy==1.16.6",
        "pycrfsuite-spacing==1.0.2",
        "scikit-learn==0.22.2.post1",
        "scipy==1.4.1",
        "seaborn==0.10.1",
        "selenium==3.141.0",
        "soynlp==0.0.493",
        "soylemma==0.2.0",
        "tensorflow==1.14.0",
        "torch",
        "tomotopy==0.8.0",
        "chatspace==1.0.1",
        "pyLDAvis==2.1.2",
        "wordcloud==1.6.0",
    ],
    python_requires='>=3.6',
)