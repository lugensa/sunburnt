import math
import pytz

from sunburnt.dates import datetime_from_w3_datestring
from sunburnt.exc import SolrError


class solr_date(object):
    """This class can be initialized from either native python datetime
    objects and mx.DateTime objects, and will serialize to a format
    appropriate for Solr"""
    def __init__(self, v):
        if isinstance(v, solr_date):
            self._dt_obj = v._dt_obj
        elif isinstance(v, basestring):
            try:
                self._dt_obj = datetime_from_w3_datestring(v)
            except ValueError, e:
                raise SolrError(*e.args)
        elif hasattr(v, "strftime"):
            self._dt_obj = self.from_date(v)
        else:
            raise SolrError("Cannot initialize solr_date from %s object"
                            % type(v))

    @staticmethod
    def from_date(dt_obj):
        # Python datetime objects may include timezone information
        if hasattr(dt_obj, 'tzinfo') and dt_obj.tzinfo:
            # but Solr requires UTC times.
            if pytz:
                return dt_obj.astimezone(pytz.utc).replace(tzinfo=None)
            else:
                raise EnvironmentError("pytz not available, cannot do timezone conversions")
        else:
            return dt_obj

    @property
    def microsecond(self):
        if hasattr(self._dt_obj, "microsecond"):
            return self._dt_obj.microsecond
        else:
            return int(1000000*math.modf(self._dt_obj.second)[0])

    def __repr__(self):
        return repr(self._dt_obj)

    def __unicode__(self):
        """ Serialize a datetime object in the format required
        by Solr. See http://wiki.apache.org/solr/IndexingDates
        """
        if hasattr(self._dt_obj, 'isoformat'):
            return "%sZ" % (self._dt_obj.isoformat(), )
        strtime = self._dt_obj.strftime("%Y-%m-%dT%H:%M:%S")
        microsecond = self.microsecond
        if microsecond:
            return u"%s.%06dZ" % (strtime, microsecond)
        return u"%sZ" % (strtime,)

    def __cmp__(self, other):
        try:
            other = other._dt_obj
        except AttributeError:
            pass
        if self._dt_obj < other:
            return -1
        elif self._dt_obj > other:
            return 1
        else:
            return 0
