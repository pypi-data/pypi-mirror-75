from setuptools import setup, find_packages

setup(
    name="nlp_utils",
    version="0.5.0",
    packages=find_packages(exclude=["tests.*"]),
    url="",
    license="MIT",
    author="Xiaoquan Kong",
    author_email="u1mail2me@gmail.com",
    description="Utils for NLP",
    install_requires=["nltk", "numpy", "tensorflow", "micro_toolkit"],
)
