from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="BERTify",
    version="0.0.1",
    description="BERT embedding extractor for bengali / english data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="Khalid Saifullah",
    author_email="khalidsaifullaah.github.io",
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python'
    ],
    install_requires=required,
    package_data={'': ['*']},
    python_requires='>=3.5',
)