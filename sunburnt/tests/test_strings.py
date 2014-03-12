from sunburnt.strings import (RawString, WildcardString)
from sunburnt.search import LuceneQuery


def test_string_escape():
    """ Ensure that string characters are escaped correctly for Solr queries.
    """
    test_str = u'+-&|!(){}[]^"~*?: \t\v\\/'
    escaped = RawString(test_str).escape_for_lqs_term()
    assert escaped == u'\\+\\-\\&\\|\\!\\(\\)\\{\\}\\[\\]\\^\\"\\~\\*\\?\\:\\ \\\t\\\x0b\\\\\\/'


def test_wildcard_string():
    q = LuceneQuery()
    q = q.Q(WildcardString(u'occurrencetype$$pressemitteilung$$*'))
    output = {None: u'occurrencetype$$pressemitteilung$$*'}
    assert q.options() == output, "Unequal: %r, %r" % (q.options(), output)
