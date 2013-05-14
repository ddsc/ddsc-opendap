from setuptools import setup

version = '0.1dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'cassandralib',
    'ddsc-core',
    'django-cors-headers',
    'django-extensions',
    'django-nose',
    'lizard-security',
    'numpy',
    'pydap',
    'pydap.responses.netcdf',
    'python-memcached',
    'tslib',
    ],

tests_require = [
    ]

setup(name='ddsc-opendap',
      version=version,
      description="OpeNDAP server for DDSC data",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='Berto Booijink',
      author_email='berto.booijink@nelen-schuurmans.nl',
      url='https://github.com/ddsc/ddsc-opendap',
      license='MIT',
      packages=['ddsc_opendap'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
