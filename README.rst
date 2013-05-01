ddsc-opendap
==========================================



Development
===========

ddsc-opendap uses a lot of Django stuff, but it is not a Django site. It may
appear easier to have made this a Django site, but it is not. Trust me. The
good news is that the ddsc-opendap server is runnable by gunicorn. For dev
machines this is the one-liner you need:

DJANGO_SETTINGS_MODULE=ddsc_api.developmentsettings \
    bin/gunicorn -b 127.0.0.1:8002 --workers 1 ddsc_opendap.handlers

