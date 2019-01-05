# -*- coding: ascii -*-
"""
styles.apa
~~~~~~~~~~

Generate APA style for article.
"""

from . import parse_author, parse_year

__all__ = ['APA']


def gen_author(author, group_author=None):
    """
    Generates authors string in APA format.

    :param author:          input author field, required
    :type author:           str
    :param group_author:    input group_author field, default is None
    :type group_author:     str or None
    :return:                String of authors in APA format
    :rtype:                 str
    """

    authors = parse_author(author, surname_sep=', ',
                           initial_sep=' ', initial_suffix='.')

    if group_author:
        authors.append(group_author.title())

    # Generate and return string of authors in APA format
    if authors:
        if len(authors) > 1:
            if len(authors) > 7:
                sep = '...'
                stop = 6
            else:
                sep = '&'
                stop = -1
            ret = '%s, %s %s' % (', '.join(authors[:stop]), sep, authors[-1])
        else:
            ret = authors[0]
        if not ret.endswith('.'):
            ret += '.'
        return ret

    # Return empty if no author found
    return ''


def gen_date(date, year=None):
    """
    Generates date in APA format (currently outputs only year).

    :param date:    input date, required
    :type date:     str
    :param year:    input year, default is None
    :type year:     str or None
    :return:        date annotation in APA format
    :rtype:         str
    """

    year = parse_year(year) or parse_year(date)
    if year:
        return ' (%s).' % year
    return ''


def gen_title(title, special_issue=None):
    """
    Generates article title in APA format.

    :param title:           original title
    :type title:            str
    :param special_issue:   special issue number of article, default is None
    :type special_issue:    str or None
    :return:                title plus special issue (if any) printed in APA format
    :rtype:                 str
    """

    ret = ''
    if title:
        ret += ' %s' % title.capitalize()
        if special_issue:
            ret += ' [%s]' % special_issue
        if not ret.endswith('.'):
            ret += '.'
    return ret


def gen_journal(title, volume, issue, begin_page, end_page):
    """
    Generates journal (periodical) information in APA format.

    :param title:       journal title
    :type title:        str
    :param volume:      journal volume number
    :type volume:       str
    :param issue:       specific issue number of volume
    :type issue:        str
    :param begin_page:  start page
    :type begin_page:   str
    :param end_page:    end page
    :type end_page:     str
    :return:            journal info in APA format
    :rtype:             str
    """

    ret = ''
    if title:
        ret += ' %s' % title.title()
        if volume and issue:
            ret += ', %s(%s)' % (volume, issue)
        elif volume:
            ret += ', %s' % volume
        elif issue:
            ret += ', (%s)' % issue
        if begin_page:
            if end_page and end_page != '+':
                ret += ', %s-%s' % (begin_page, end_page)
            else:
                ret += ', %s' % begin_page
        if not ret.endswith('.'):
            ret += '.'
    return ret


def gen_doi(doi):
    """Generates DOI number in APA format using original DOI."""
    return ' doi:%s' % doi if doi else ''


def gen_location(location):
    """Generates location string in APA format from original location."""
    if location:
        location = ' Paper presented at %s' % location
        if not location.endswith('.'):
            location += '.'
        return location
    return ''


class APA:
    _fmt = '{author}{date}{title}{last}'
    _fmt_no_author = '{title}{date}{last}'

    def __init__(self, **kwargs):
        self.journal = ''
        self.conference = ''

        has_author = bool(kwargs.get('author') or kwargs.get('group_author'))
        has_journal = bool(kwargs.get('article_title'))
        has_conference = bool(kwargs.get('conf_title'))

        fmt = self._fmt if has_author else self._fmt_no_author
        author = gen_author(kwargs.get('author'), kwargs.get('group_author'))

        if has_journal:
            self.journal = fmt.format(
                author=author,
                date=gen_date(kwargs.get('pub_date'), kwargs.get('pub_year')),
                title=gen_title(kwargs.get('article_title'),
                                kwargs.get('special_issue')),
                last=gen_journal(kwargs.get('pub_name'), kwargs.get('volume'),
                                 kwargs.get('issue'), kwargs.get('begin_page'),
                                 kwargs.get('end_page'))
            ).strip()

        if has_conference:
            self.conference = fmt.format(
                author=author,
                date=gen_date(kwargs.get('conf_date')),
                title=gen_title(kwargs.get('conf_title')),
                last=gen_location(kwargs.get('conf_location'))
            ).strip()
