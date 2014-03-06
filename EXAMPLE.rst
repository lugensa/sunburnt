Example
=======

Example usage with requests::

    >>> import sunburnt.search
    >>> import urllib
    >>> import requests
    >>> q = sunburnt.search.SolrSearch()
    >>> search  = q.query("hello world").filter(q.Q(text_field="tow") & q.Q(boolean_field=False, int_field__gt=3))
    >>> search.params()
    [('fq', 'boolean_field:false'),
     ('fq', 'int_field:{3 TO *}'),
     ('fq', 'text_field:tow'),
     ('q', 'hello\\ world')]
    >>> params = search.params()
    >>> urllib.urlencode(params)
    'fq=boolean_field%3Afalse&fq=int_field%3A%7B3+TO+%2A%7D&fq=text_field%3Atow&q=hello%5C+world'
    >>> requests.post(...)



