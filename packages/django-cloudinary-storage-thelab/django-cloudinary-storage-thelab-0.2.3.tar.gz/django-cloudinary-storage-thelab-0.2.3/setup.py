import codecs
import os
from os import path

from setuptools import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-cloudinary-storage-thelab',
    version='0.2.3',
    author='Konrad Lisiczynski',
    author_email='klisiczynski@gmail.com',
    license='MIT',
    url='https://github.com/klis87/django-cloudinary-storage',
    keywords='django cloudinary storage',
    packages=[
        'cloudinary_storage',
        'cloudinary_storage.templatetags',
        'cloudinary_storage.management',
        'cloudinary_storage.management.commands'],
    include_package_data=True,
    install_requires=[
        'requests>=2.23.0',
        'cloudinary>=1.20.0'
    ],
    extras_require={
        'video': ['python-magic>=0.4.12']
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
