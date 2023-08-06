from setuptools import setup
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()
setup(
name = "pyGoogleTranslate",
packages = ["pyGoogleTranslate"],
version = "3.5.1",
license = "MIT",
description = "A python module which lets you use Google Translate (translation, transliteration, defintion, language detection, etc.) by parsing the website.",
author = "Anime no Sekai",
author_email = "niichannomail@gmail.com",
url = "https://github.com/Animenosekai/pyGoogleTranslate",
download_url = "https://github.com/Animenosekai/pyGoogleTranslate/archive/v3.5.1.tar.gz",
keywords = ['translate', 'translation', 'google_translate', 'google', 'selenium', 'animenosekai'],
install_requires = ['selenium', 'lifeeasy', 'psutil'],
classifiers = ['Development Status :: 5 - Production/Stable', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8'],
long_description = readme_description,
long_description_content_type = "text/markdown",
include_package_data=True
)
