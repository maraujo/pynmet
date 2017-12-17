from setuptools import setup, find_packages
import re

with open('pynmet/__init__.py', encoding='utf-8') as f:
    version = re.search(r"__version__\s*=\s*'(\S+)'", f.read()).group(1)


classifiers = ['Development Status :: 2 - Pre-Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: Python Software Foundation License',
               'License :: OSI Approved :: GNU General Public License (GPL)',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name = 'pynmet',
      version = version,
      author = 'Josué M. Sehnem',
      author_email = 'josue@sehnem.com',
      description = 'Python code to retrieve and plot inmet meteorological data',
      license = 'GPLv3+',
      classifiers = classifiers,
      url = 'https://github.com/sehnem/pynmet/',
      download_url = 'https://github.com/sehnem/pynmet/archive/{}.tar.gz'.format(version),
      dependency_links = [],
      install_requires = ['lxml','pandas', 'bs4', 'tables', 'click'],
      packages = find_packages(),
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      [console_scripts]
      pynmet=pynmet.cli:cli
      """
      )
