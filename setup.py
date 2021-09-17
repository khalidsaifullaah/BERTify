import pip

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

links = []
requires = []

try:
    requirements = pip.req.parse_requirements('requirements.txt')
except:
    # new versions of pip requires a session
    requirements = pip.req.parse_requirements(
        'requirements.txt', session=pip.download.PipSession())

for item in requirements:
    # we want to handle package names and also repo urls
    if getattr(item, 'url', None):  # older pip has url
        links.append(str(item.url))
    if getattr(item, 'link', None): # newer pip has link
        links.append(str(item.link))
    if item.req:
        requires.append(str(item.req))

setup(
    name="BERTify",
    version="0.0.1",
    description="BERT embedding extractor for bengali / english data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/khalidsaifullaah/BERTify',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requires,
    dependency_links=links
)