from setuptools import setup
from numtxt import VERSION

setup(name = 'numtxt',
      version = VERSION,
      description = 'gives full and approximate written forms of numbers',
      long_description = open('README.rst').read(),
      license = 'GPLv3',
      author = 'Philip Herd',
      url = 'http://github.com/Electrostatus/numtxt',
      py_modules = ['numtxt'],
      keywords = 'approximation written word number name numeral si prefix cardinal ordinal precedence',
      package_data = {'': ['*.rst']},
      classifiers = [
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        ],
      )
