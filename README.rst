ddsc-opendap
==========================================


Usage
=====

DDSC timeseries are accessable through the OpenDAP protocol at:

http://api.dijkdata.nl/opendap/<UUID>.<EXT>

<UUID> The unique identifier of a timeseries.
<EXT>  Format to receive the data in. Valid options:
       - dods        : OpenDAP binary
       - asc / ascii : OpenDAP ASCII
       - nc          : NetCDF
       - html        : HTML form to specify filters and format

Example:

http://api.dijkdata.nl/opendap/aaa33d42-ad50-4d52-aae3-63b93446dab4.nc

For convenience, each Timeseries' details in the REST API at
http://api.dijkdata.nl/api/v*/timeseries/<UUID>
includes a hyperlink to that Timeseries' OpenDAP equivalent at
http://api.dijkdata.nl/opendap/<UUID>.html

The DDSC OpenDAP server supports authentication by http headers. Requests
should include header fields 'Username' and 'Password' with the appropriate
content.


Development
===========

ddsc-opendap uses a lot of Django stuff, but it is not a Django site. It may
appear easier to have made this a Django site, but it is not. Trust me. The
good news is that the ddsc-opendap server is runnable by gunicorn. For dev
machines this is the one-liner you need:

DJANGO_SETTINGS_MODULE=ddsc_api.developmentsettings \
    bin/gunicorn -b 127.0.0.1:8002 --workers 1 ddsc_opendap.handlers

