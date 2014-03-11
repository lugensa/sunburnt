import datetime
import math
import re
import pytz
from sunburnt.exc import SolrError

try:
    import mx.DateTime
    HAS_MX_DATETIME = True
except ImportError:
    HAS_MX_DATETIME = False


year = r'[+/-]?\d+'
tzd = r'Z|((?P<tzd_sign>[-+])(?P<tzd_hour>\d\d):(?P<tzd_minute>\d\d))'
extended_iso_template = r'(?P<year>' + year + r""")
               (-(?P<month>\d\d)
               (-(?P<day>\d\d)
            ([T%s](?P<hour>\d\d)
                :(?P<minute>\d\d)
               (:(?P<second>\d\d)
               (.(?P<fraction>\d+))?)?
               (""" + tzd + """)?)?
               )?)?"""
extended_iso = extended_iso_template % " "
extended_iso_re = re.compile('^' + extended_iso + '$', re.X)


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


def datetime_from_w3_datestring(s):
    """ We need to extend ISO syntax (as permitted by the standard) to allow
    for dates before 0AD and after 9999AD. This is how to parse such a string
    """
    m = extended_iso_re.match(s)
    if not m:
        raise ValueError
    d = m.groupdict()
    d['year'] = int(d['year'])
    d['month'] = int(d['month'] or 1)
    d['day'] = int(d['day'] or 1)
    d['hour'] = int(d['hour'] or 0)
    d['minute'] = int(d['minute'] or 0)
    d['fraction'] = d['fraction'] or '0'
    d['second'] = float("%s.%s" % ((d['second'] or '0'), d['fraction']))
    del d['fraction']
    if d['tzd_sign']:
        if d['tzd_sign'] == '+':
            tzd_sign = 1
        elif d['tzd_sign'] == '-':
            tzd_sign = -1
        try:
            tz_delta = datetime_delta_factory(tzd_sign * int(d['tzd_hour']),
                                              tzd_sign * int(d['tzd_minute']))
        except DateTimeRangeError as e:
            raise ValueError(e.args[0])
    else:
        tz_delta = datetime_delta_factory(0, 0)
    del d['tzd_sign']
    del d['tzd_hour']
    del d['tzd_minute']
    d['tzinfo'] = pytz.utc
    try:
        dt = datetime_factory(**d) + tz_delta
    except DateTimeRangeError as e:
        raise ValueError(e.args[0])
    return dt


class DateTimeRangeError(ValueError):
    pass


if HAS_MX_DATETIME:
    def datetime_factory(**kwargs):
        try:
            return mx.DateTime.DateTimeFrom(**kwargs)
        except mx.DateTime.RangeError as e:
            raise DateTimeRangeError(e.args[0])
else:
    def datetime_factory(**kwargs):
        second = kwargs.get('second')
        if second is not None:
            f, i = math.modf(second)
            kwargs['second'] = int(i)
            kwargs['microsecond'] = int(f * 1000000)
        try:
            return datetime.datetime(**kwargs)
        except ValueError, e:
            raise DateTimeRangeError(e.args[0])

if HAS_MX_DATETIME:
    def datetime_delta_factory(hours, minutes):
        return mx.DateTime.DateTimeDelta(0, hours, minutes)
else:
    def datetime_delta_factory(hours, minutes):
        return datetime.timedelta(hours=hours, minutes=minutes)


class solr_date(object):
    """This class can be initialized from either native python datetime
    objects and mx.DateTime objects, and will serialize to a format
    appropriate for Solr"""
    def __init__(self, v):
        if isinstance(v, solr_date):
            self._dt_obj = v._dt_obj
        elif isinstance(v, basestring):
            self._dt_obj = datetime_from_w3_datestring(v)
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
