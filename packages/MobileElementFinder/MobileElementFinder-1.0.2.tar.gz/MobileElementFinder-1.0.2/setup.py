from distutils.util import convert_path

from setuptools import find_packages, setup
import os

PACKAGE_DIR = 'me_finder'

setup(name='MobileElementFinder',
      version='1.0.2',
      description='Mobile Genetic Element prediction',
      long_description_markdown_filename='README.md',
      long_description_content_type='text/markdown',
      url='https://bitbucket.org/mhkj/mge_finder/src/master/',
      author='Markus Johansson',
      author_email='markjo@food.dtu.dk',
      license='GPLv3',
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      entry_points={'console_scripts': ['mefinder=me_finder.cli:cli']},
      include_package_data=True,
      package_data={'me_finder': ['%s/logging.yml' % PACKAGE_DIR,
                                  '%s/config.ini' % PACKAGE_DIR]},
      packages=find_packages(exclude=('tests', 'scripts')))
