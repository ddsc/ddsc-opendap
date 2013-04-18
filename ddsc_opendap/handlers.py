# (c) Nelen & Schuurmans.  MIT licensed, see LICENSE.rst.
#from __future__ import unicode_literals

from django.conf import settings
from ddsc_opendap import settings as mysettings # TODO: differentiate envs
settings.configure(**mysettings.__dict__)

import re
import numpy as np
import time

from datetime import datetime
from pydap.model import SequenceData, SequenceType, DatasetType, BaseType, Float32, Int32
from pydap.handlers.lib import BaseHandler
from ddsc_core.models import Timeseries

COLNAME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class CassandraHandler(BaseHandler):

    def __init__(self, dummy):
        BaseHandler.__init__(self)
        self.uuid = ''

    def parse_constraints(self, environ):
        uuid = environ.get('pydap.path', '')

        # Build the dataset object.
        dataset = DatasetType('timeseries')

        # Build the sequence object, and insert it in the dataset.
        seq = SequenceType(uuid)
        seq['datetime'] = BaseType(name='datetime', type=Int32)
        seq['value'] = BaseType(name='value', type=Float32)
        seq['flag'] = BaseType(name='flag', type=Int32)
        seq.data = CassandraData(uuid, ['datetime', 'value', 'flag'])

        dataset[seq.name] = seq

        query = environ.get('QUERY_STRING', '')

#        return seq
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
        start = datetime.strptime('2009-01-01T23:00:00Z', COLNAME_FORMAT)
        end = datetime.strptime('2009-01-11T23:00:00Z', COLNAME_FORMAT)

        df = self.ts.get_events(start=start, end=end, filter=self.selection)
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


if __name__ == '__main__':
    import sys
    from paste.httpserver import serve

    application = CassandraHandler('')
    serve(application, host='0.0.0.0', port=8001)
