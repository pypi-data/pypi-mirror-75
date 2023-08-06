from setuptools import setup
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()
setup(
name = "pyGoogleTranslate",
packages = ["pyGoogleTranslate"],
version = "2.0",
license = "MIT",
description = "A little python to parse Google Translate webpages",
author = "Anime no Sekai",
author_email = "niichannomail@gmail.com",
url = "https://github.com/Animenosekai/python_google_translate",
download_url = "https://github.com/Animenosekai/python_google_translate/archive/v2.0.tar.gz",
keywords = ['translate', 'translation', 'google_translate', 'google', 'selenium', 'animenosekai'],
install_requires = ['selenium'],
classifiers = ['Development Status :: 4 - Beta', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8'],
long_description = readme_description,
long_description_content_type = "text/markdown",
)
