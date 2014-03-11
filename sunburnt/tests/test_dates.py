import datetime

try:
    import mx.DateTime
    HAS_MX_DATETIME = True
except ImportError:
    HAS_MX_DATETIME = False
import pytz

from sunburnt.dates import solr_date

not_utc = pytz.timezone('Etc/GMT-3')

samples_from_pydatetimes = {
    "2009-07-23T03:24:34.000376Z":
    [datetime.datetime(2009, 07, 23, 3, 24, 34, 376),
     datetime.datetime(2009, 07, 23, 3, 24, 34, 376, pytz.utc)],
    "2009-07-23T00:24:34.000376Z":
    [not_utc.localize(datetime.datetime(2009, 07, 23, 3, 24, 34, 376)),
     datetime.datetime(2009, 07, 23, 0, 24, 34, 376, pytz.utc)],
    "2009-07-23T03:24:34Z":
    [datetime.datetime(2009, 07, 23, 3, 24, 34),
     datetime.datetime(2009, 07, 23, 3, 24, 34, tzinfo=pytz.utc)],
    "2009-07-23T00:24:34Z":
    [not_utc.localize(datetime.datetime(2009, 07, 23, 3, 24, 34)),
     datetime.datetime(2009, 07, 23, 0, 24, 34, tzinfo=pytz.utc)]
}

if HAS_MX_DATETIME:
    samples_from_mxdatetimes = {
        "2009-07-23T03:24:34.000376Z":
        [mx.DateTime.DateTime(2009, 07, 23, 3, 24, 34.000376),
         datetime.datetime(2009, 07, 23, 3, 24, 34, 376, pytz.utc)],
        "2009-07-23T03:24:34Z":
        [mx.DateTime.DateTime(2009, 07, 23, 3, 24, 34),
         datetime.datetime(2009, 07, 23, 3, 24, 34, tzinfo=pytz.utc)],
    }


samples_from_strings = {
    # These will not have been serialized by us, but we should deal with them
    "2009-07-23T03:24:34Z":
    datetime.datetime(2009, 07, 23, 3, 24, 34, tzinfo=pytz.utc),
    "2009-07-23T03:24:34.1Z":
    datetime.datetime(2009, 07, 23, 3, 24, 34, 100000, pytz.utc),
    "2009-07-23T03:24:34.123Z":
    datetime.datetime(2009, 07, 23, 3, 24, 34, 122999, pytz.utc)
}


def check_solr_date_from_date(s, date, canonical_date):
    assert unicode(solr_date(date)) == s, "Unequal representations of %r: %r and %r" % (
        date, unicode(solr_date(date)), s)
    check_solr_date_from_string(s, canonical_date)


def check_solr_date_from_string(s, date):
    assert solr_date(s)._dt_obj == date, "Unequal representations of %r: %r" % (
        solr_date(s)._dt_obj, date)


def test_solr_date_from_pydatetimes():
    for k, v in samples_from_pydatetimes.items():
        yield check_solr_date_from_date, k, v[0], v[1]


def test_solr_date_from_mxdatetimes():
    if HAS_MX_DATETIME:
        for k, v in samples_from_mxdatetimes.items():
            yield check_solr_date_from_date, k, v[0], v[1]


def test_solr_date_from_strings():
    for k, v in samples_from_strings.items():
        yield check_solr_date_from_string, k, v
