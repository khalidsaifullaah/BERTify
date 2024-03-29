from setuptools import setup

with open("README.md", 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# with open('requirements.txt') as f:
#     requirements = f.read().splitlines()

setup(
    name="BERTify",
    version="0.0.3",
    description="BERT embedding extractor for bengali / english data.",
    author='Khalid Saifullah',
    author_email='ksaifullah172043@bscse.uiu.ac.bd',
    packages=['bertify'],
    url='https://github.com/khalidsaifullaah/BERTify',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "numpy",
        "torch",
        "tqdm",
        "transformers",
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python'
    ],
    package_data={'': ['*']},
    python_requires='>=3.5',
)