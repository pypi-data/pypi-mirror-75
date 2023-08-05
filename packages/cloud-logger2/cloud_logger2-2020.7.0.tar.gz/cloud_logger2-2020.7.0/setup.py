#!/usr/bin/env python
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cloud_logger2',
    version='2020.7.0',
    author='artemdevel',
    author_email='artem.devel2014@gmail.com',
    description='An experimental lightweight logger',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/artemdevel/cloud_logger',
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
