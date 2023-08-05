#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

Dir = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(Dir, "robomentor_client", '__config__.py')) as f:
    exec(f.read(), about)

version = about["__version__"]

try:
    with io.open(os.path.join(Dir, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = ''


class UploadCommand(Command):

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(Dir, 'dist'))
        except OSError:
            pass

        self.status('Preparing {0} v{1}...' . format('RoboMentor_Client', version))

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name='RoboMentor_Client',
    version=version,
    description='Python library and framework for robomentor_client.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Super Yang',
    author_email='admin@wileho.com',
    python_requires='>=3.6.0',
    url='https://github.com/robomentor/RoboMentor_Client',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=[
        'paho-mqtt',
        'psutil',
        'rpi.gpio'
    ],
    extras_require={
        'python 3.6.x needs': ['dataclasses'],
    },
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    cmdclass={
        'upload': UploadCommand,
    }
)
