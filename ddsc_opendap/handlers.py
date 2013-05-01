# (c) Nelen & Schuurmans.  MIT licensed, see LICENSE.rst.
#from __future__ import unicode_literals

import re
import numpy as np
import time

from datetime import datetime
from django.contrib.auth import authenticate
from pydap.handlers.helper import constrain
from pydap.handlers.lib import BaseHandler
from pydap.model import SequenceData, SequenceType, DatasetType, BaseType, Float32, Int32

from ddsc_core.models import Timeseries

COLNAME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class CassandraHandler(BaseHandler):

    def parse_constraints(self, environ):
        # Build the dataset object.
        dataset = DatasetType('timeseries')

        user = None
        username = environ.get('HTTP_USERNAME', None)
        password = environ.get('HTTP_PASSWORD', None)

        if username and password:
            user = authenticate(username=username, password=password)
        if not user:
            return dataset

        uuid = environ.get('pydap.path', '')

        # Build the sequence object, and insert it in the dataset.
        seq = SequenceType(uuid)
        seq['datetime'] = BaseType(name='datetime', type=Int32)
        seq['value'] = BaseType(name='value', type=Float32)
        seq['flag'] = BaseType(name='flag', type=Int32)
        
        try:
            seq.data = CassandraData(uuid, ['datetime', 'value', 'flag'])
        except Timeseries.DoesNotExist:
            return dataset

        dataset[seq.name] = seq

        query = environ.get('QUERY_STRING', '')
        print dataset

        return constrain(dataset, environ.get('QUERY_STRING', ''))
        return dataset


class CassandraData(object):
    shape = ()

    def __init__(self, uuid, cols, selection=None, slice_=None):
        self.ts = Timeseries.objects.get(uuid=uuid)
        self.cols = cols
        self.selection = selection or []
        self.slice = slice_ or (slice(None),)

    @property
    def dtype(self):
        print "dtype"
        peek = iter(self).next()
        return np.array(peek).dtype

    def __iter__(self):
        print "__iter__"
        df = self.ts.get_events(start=None, end=None, filter=self.selection)
        for dt, row in df.iterrows():
            yield (377+1000*long(time.mktime(dt.timetuple())), row['value'], row['flag'])

    def __getitem__(self, key):
        print "__getitem__ %s" % key
        out = self.clone()

        # return the data for a children
        if isinstance(key, basestring):
            out.id = '{id}.{child}'.format(id=self.uuid, child=key)
            out.cols = key

        # return a new object with requested columns
        elif isinstance(key, list):
            out.cols = tuple(key)

        # return a copy with the added constraints
        elif isinstance(key, ConstraintExpression):
            out.selection.extend( str(key).split('&') )

        # slice data
        else:
            if isinstance(key, int):
                key = slice(key, key+1)
            out.slice = combine_slices(self.slice, (key,))

        print out
        return out

    def clone(self):
        print "clone %s" % self
        return self.__class__(self.uuid, self.cols[:], self.selection[:],
                              self.slice[:])

    def __eq__(self, other): return ConstraintExpression('%s=%s' % (self.id, encode(other)))
    def __ne__(self, other): return ConstraintExpression('%s!=%s' % (self.id, encode(other)))
    def __ge__(self, other): return ConstraintExpression('%s>=%s' % (self.id, encode(other)))
    def __le__(self, other): return ConstraintExpression('%s<=%s' % (self.id, encode(other)))
    def __gt__(self, other): return ConstraintExpression('%s>%s' % (self.id, encode(other)))
    def __lt__(self, other): return ConstraintExpression('%s<%s' % (self.id, encode(other)))


application = CassandraHandler()
