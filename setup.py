#!/usr/bin/env python

from setuptools import setup, find_packages
import muxnect

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='muxnect',
      version=muxnect.__version__,
      description='Send input to just about any interactive command-line tool through a local web server',
      long_description=long_description,
      author='Ritiek Malhotra',
      author_email='ritiekmalhotra123@gmail.com',
      packages = find_packages(),
      entry_points={
            'console_scripts': [
                  'muxnect = muxnect.server:command_line',
            ]
      },
      url='https://www.github.com/ritiek/muxnect',
      keywords=['tmux', 'connect', 'send', 'input', 'command-line', 'interactive', 'local', 'network'],
      license='MIT',
      download_url='https://github.com/ritiek/muxnect/archive/v' + muxnect.__version__ + '.tar.gz',
      classifiers=[],
      install_requires=[
            'requests',
            'Flask',
            'libtmux',
      ]
)
