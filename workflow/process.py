# -*- coding: utf-8 -*-
#
# cd /Users/josh/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows
#

import calendar

import alfred
import pytz
from delorean import utcnow, parse, epoch


def process(query_str):
    """ Entry point """
    value = parse_query_value(query_str)
    if value is not None:
        results = alfred_items_for_value(value)
        xml = alfred.xml(results)  # compiles the XML answer
        alfred.write(xml)  # writes the XML back to Alfred


def parse_query_value(query_str):
    """ Return value for the query string """
    try:
        query_str = str(query_str).strip('"\' ')
        if query_str == 'now':
            d = utcnow()
        else:
            # Parse datetime string or timestamp
            try:
                f = float(query_str)
                f_str = "{:.0f}".format(f)

                if len(f_str) > 10:
                    f = float(f_str[0:10])

                d = epoch(f)
            except ValueError:
                d = parse(str(query_str))
    except (TypeError, ValueError):
        d = None
    return d


def alfred_items_for_value(value):
    """
    Given a delorean datetime object, return a list of
    alfred items for each of the results
    """

    index = 0
    results = []

    # First item as timestamp
    item_value = calendar.timegm(value.datetime.utctimetuple())
    results.append(alfred.Item(
        title=str(item_value),
        subtitle=u'UTC Timestamp',
        attributes={
            'uid': alfred.uid(index),
            'arg': item_value,
        },
        icon='icon.png',
    ))
    index += 1

    eastern = pytz.timezone('US/Eastern')
    # loc_dt = eastern.localize(value.datetime)
    loc_dt = value.datetime.astimezone(eastern)
    est_time_str = loc_dt.strftime("%Y-%m-%d %H:%M:%S ET")

    results.append(alfred.Item(
        title=str(est_time_str),
        subtitle='',
        attributes={
            'uid': alfred.uid(index),
            'arg': est_time_str,
        },
        icon='icon.png',
    ))
    index += 1

    results.append(alfred.Item(
        title=str(value.datetime.strftime("%Y-%m-%d %H:%M:%S UTC")),
        subtitle='',
        attributes={
            'uid': alfred.uid(index),
            'arg': value.datetime.strftime("%Y-%m-%d %H:%M:%S UTC"),
        },
        icon='icon.png',
    ))
    index += 1

    est_time_str = loc_dt.strftime("%A %B %-d %Y ET")
    results.append(alfred.Item(
        title=str(est_time_str),
        subtitle='',
        attributes={
            'uid': alfred.uid(index),
            'arg': est_time_str,
        },
        icon='icon.png',
    ))
    index += 1

    results.append(alfred.Item(
        title=str(value.datetime.strftime("%A %B %-d %Y UTC")),
        subtitle='',
        attributes={
            'uid': alfred.uid(index),
            'arg': value.datetime.strftime("%A %B %-d %Y UTC"),
        },
        icon='icon.png',
    ))
    index += 1

    est_time_str = loc_dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    results.append(alfred.Item(
        title=str(est_time_str),
        subtitle='RFC3339 ET',
        attributes={
            'uid': alfred.uid(index),
            'arg': est_time_str,
        },
        icon='icon.png',
    ))
    index += 1

    # Various formats
    formats = [
        # 1937-01-01 12:00:27
        # ("%Y-%m-%d %H:%M:%S", 'UTC Time'),
        # 19 May 2002 15:21:36
        # ("%d %b %Y %H:%M:%S", ''),
        # Sun, 19 May 2002 15:21:36
        # ("%a, %d %b %Y %H:%M:%S", ''),
        # 1937-01-01T12:00:27
        # ("%Y-%m-%dT%H:%M:%S", ''),
        # 1996-12-19T16:39:57-0800
        ("%Y-%m-%dT%H:%M:%S%z", 'RFC3339 UTC'),
    ]
    for format, description in formats:
        item_value = value.datetime.strftime(format)
        results.append(alfred.Item(
            title=str(item_value),
            subtitle=description,
            attributes={
                'uid': alfred.uid(index),
                'arg': item_value,
            },
            icon='icon.png',
        ))
        index += 1

    return results


if __name__ == "__main__":
    # try:
    #     query_str = alfred.args()[0]
    # except IndexError:
    #     query_str = None
    # process(query_str)
    process("now")
