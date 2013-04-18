DATABASES = {
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
        'localhost:9160',
#        '192.168.20.13:9160', #virtual box
#        '10.100.235.201:9160',
#        '10.100.235.202:9160',
#        '10.100.235.203:9160',
#        '10.100.235.204:9160',
#        '192.168.1.154:9160',
#        '192.168.1.153:9160',
#        '192.168.1.148:9160',
#        '192.168.1.150:9160',
    ],
    'keyspace': 'ddsc',
    'batch_size': 10000,
}

RABBITMQ = {
    'server': 'p-flod-rmq-d1.external-nens.local',
    'vhost': 'ddsc-development',
    'user': 'ddsc',
    'password': 'evaiurhaiu'
}

FILE_DIR = 'var/data'

# SSO
SSO_STANDALONE = False
SSO_ENABLED = True
# A key identifying this client. Can be published.
SSO_KEY = '0Roslimzqh7qglHjZMEuJRiIx9p3shPzsrgDoAZNVSqBXCntP9ZiNpXlZ4ez1KBG'
# A *secret* shared between client and server. Used to sign the messages exchanged between them.
SSO_SECRET = 'VFctvyxo3V7t6J2qALJfZ1EcOUADk8t0XVXFJgdF8VYkIopR8EF0KezOHZXxKmv8'
# URL used to redirect the user to the SSO server
# Note: needs a trailing slash
SSO_SERVER_PUBLIC_URL = 'https://sso.lizard.net/'
# URL used for server-to-server communication
# Note: needs a trailing slash
SSO_SERVER_PRIVATE_URL = 'http://p-web-ws-00-d8.external-nens.local:9874/'

