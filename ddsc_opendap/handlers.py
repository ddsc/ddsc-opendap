# (c) Nelen & Schuurmans.  MIT licensed, see LICENSE.rst.
#from __future__ import unicode_literals

import pydap.responses.html
from pydap.util.template import GenshiRenderer, StringLoader

DEFAULT_TEMPLATE = pydap.responses.html.DEFAULT_TEMPLATE \
    .replace("&copy; Roberto De Almeida", "") \
    .replace("<em><a href=\"http://pydap.org/\">pydap/$version</a></em>", "")
pydap.responses.html.HTMLResponse.renderer = GenshiRenderer(
    options={}, loader=StringLoader( {'html.html': DEFAULT_TEMPLATE} ))

import Cookie
import re
import numpy as np
import time

from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from pydap.handlers.helper import constrain
from pydap.handlers.lib import BaseHandler
from pydap.model import StructureType, SequenceType, DatasetType, BaseType
from pydap.model import SequenceData, Float32, Int32
from urllib import unquote

from ddsc_core.models import Timeseries

COLNAME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class RootHandler(BaseHandler):
    def __call__(self, environ, start_response):
        try:
            return EventHandler().__call__(environ, start_response)
        except Exception as ex:
            return "Permission denied"


class EventHandler(BaseHandler):
    
    def parse_constraints(self, environ):
        # Build the dataset object.
        dataset = DatasetType('timeseries')

        user = None
        username = environ.get('HTTP_USERNAME', None)
        password = environ.get('HTTP_PASSWORD', None)

        if username and password:
            user = authenticate(username=username, password=password)

        if not user:
            cookie_string = environ.get('HTTP_COOKIE', None)
            if cookie_string:
                cookie = Cookie.SimpleCookie()
                cookie.load(cookie_string)
                if 'sessionid' in cookie:
                    sessionid = cookie['sessionid'].value
                    try:
                        session = Session.objects.get(pk=sessionid)
                        session_data = session.get_decoded()
                        if '_auth_user_id' in session_data:
                            userid = session_data['_auth_user_id']
                            user = User.objects.get(pk=userid)
                    except Session.DoesNotExist, User.DoesNotExist:
                        pass

        if not user:
            return dataset

        path = environ.get('pydap.path', '').split('/')
        uuid = path[-1]

        # Build the sequence object, and insert it in the dataset.
        seq = SequenceType(uuid)
        seq['datetime'] = BaseType(name='datetime', type=Float32)
        seq['value'] = BaseType(name='value', type=Float32)
        seq['flag'] = BaseType(name='flag', type=Int32)
        
        try:
            seq.data = EventData(uuid, ['datetime', 'value', 'flag'])
        except Timeseries.DoesNotExist:
            return dataset

        dataset[seq.name] = seq

        return constrain(dataset, environ.get('QUERY_STRING', ''))


class EventData(object):

    def __init__(self, uuid, cols, selection=None, slice_=None):
        self.ts = Timeseries.objects.get(uuid=uuid)
        self.cols = cols
        self.selection = selection or []
        self.slice = slice_ or (slice(None),)
        self.df = self.ts.get_events(start=None, end=None, filter=self.selection)

    @property
    def dtype(self):
        peek = iter(self).next()
        return np.array(peek).dtype

    def __iter__(self):
        for dt, row in self.df.iterrows():
            yield (dt.strftime('%s.%f'), row['value'], row['flag'])

    def __len__(self):
        return len(self.df)


application = RootHandler()
