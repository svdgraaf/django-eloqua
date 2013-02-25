#!/usr/bin/env python
from setuptools import setup, find_packages

try:
    README = open('README.rst').read()
except:
    README = None

try: 
    LICENSE = open('LICENSE.txt').read()
except: 
    LICENSE = None

setup(
    name = 'django-eloqua',
    version = '0.3.5',
    description='Python/Django interface for the Eloqua REST api.',
    long_description=README,
    author = 'Sander van de Graaf',
    author_email = 'mail@svdgraaf.nl',
    license = LICENSE,
    url = 'http://github.com/svdgraaf/django-eloqua/',
    packages = find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
    ],
    install_requires=[
        "Django >= 1.3.0",
        "requests >= 1.1.0",

    ],
)
