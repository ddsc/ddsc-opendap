import os

from lizard_ui.settingshelper import setup_logging

from ddsc_opendap.settings import *

DEBUG = True

# By default, var/log/django.log gets WARN level logging, the console gets
# DEBUG level logging.
LOGGING = setup_logging(BUILDOUT_DIR)

# ENGINE: 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
# In case of geodatabase, prepend with:
# django.contrib.gis.db.backends.(postgis)
DATABASES = {
    # If you want to use another database, consider putting the database
    # settings in localsettings.py. Otherwise, if you change the settings in
    # the current file and commit them to the repository, other developers will
    # also use these settings whether they have that database or not.
    # One of those other developers is Jenkins, our continuous integration
    # solution. Jenkins can only run the tests of the current application when
    # the specified database exists. When the tests cannot run, Jenkins sees
    # that as an error.
    'default': {
        'NAME': 'ddsc_api',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': 'buildout',
        'PASSWORD': 'buildout',
        'HOST': '',  # empty string for localhost.
        'PORT': '',  # empty string for default.
        }
    }

CASSANDRA = {
    'servers': [
        '10.100.235.201:9160',
        '10.100.235.202:9160',
        '10.100.235.203:9160',
        '10.100.235.204:9160'
        ],
    'keyspace': 'ddsc',
    'batch_size': 10000,
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BUILDOUT_DIR, 'var', 'cache'),
    }
}

try:
    from ddsc_opendap.localsettings import *  # NOQA
except ImportError:
    pass
