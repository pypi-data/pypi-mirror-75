import os
import re
from setuptools import setup, find_packages
from io import open



setup(
    name = 'cfscraper',
    author = '',
    author_email = '',
    version='0.14',
    packages = find_packages(exclude=['tests*']),
    description = 'A Python module to bypass Cloudflare\'s anti-bot page.',
 
   
    include_package_data = True,
    install_requires = [
        'requests >= 2.9.2',
        'requests_toolbelt >= 0.9.1',
        'pyparsing >= 2.4.7'
    ]
)
