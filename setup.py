# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pypandoc
    LDESC = open('README.md', 'r').read()
    LDESC = pypandoc.convert(LDESC, 'rst', format='md')
except (ImportError, IOError, RuntimeError) as e:
    print("Could not create long description:")
    print(str(e))
    LDESC = ''

setup(name='serialman',
      version = '0.1',
      description = 'serialman = PySerial Manager : A Python package facilitating the use of PySerial.',
      long_description = LDESC,
      author = 'Philipp Klaus',
      author_email = 'philipp.l.klaus@web.de',
      url = 'https://github.com/pklaus/serialman',
      license = 'GPL',
      #packages = ['',],
      py_modules = ['serialman',],
      #entry_points = {
      #    'console_scripts': [
      #        'serialman = serialman:main',
      #    ],
      #},
      zip_safe = True,
      platforms = 'any',
      install_requires = [
          "PySerial",
      ],
      keywords = 'PySerial Manager',
      classifiers = [
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Hardware :: Hardware Drivers',
      ]
)

