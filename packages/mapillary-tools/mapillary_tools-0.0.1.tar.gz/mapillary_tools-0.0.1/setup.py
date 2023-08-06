#!/usr/bin/env python

from setuptools import setup

setup (
    name='mapillary_tools',
    version='0.0.1',
    description='Mapillary Commandline Image Uploader',
    keywords='mapillary commandline console image upload',
    url='https://github.com/MarcelloPerathoner/mapillary_tools',
    author='Marcello Perathoner',
    author_email='marcello@perathoner.de',
    license='GPL3',
    python_requires='>=3.5.0',
    packages=['mapillary_tools'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ],
    scripts=[
        'bin/mapillary_auth.py',
        'bin/mapillary_process.py',
        'bin/mapillary_upload.py',
    ],
    install_requires=[
        'geopy',
        'piexif',
        'requests',
        'tqdm',
    ],
)
