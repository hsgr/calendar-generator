#!/usr/bin/env python
#
#
#
import json
import urllib
import string
import htmllib
from datetime import datetime, timedelta

import googl

QUERY = "http://hackerspace.gr/api.php?action=ask&q=[[Category:Events]]" \
        "&format=json&po=location|Start%20date"

HEADER = string.join(("BEGIN:VCALENDAR",
                     "PRODID:-//Hackerspace.gr Events//hackerspace.gr//",
                     "VERSION:2.0"),
                     "\r\n"
                     )

FOOTER = "END:VCALENDAR"

def unescape(s):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()

def main():
    try:
        results = urllib.urlopen(QUERY).read()

    except:
        raise

    results = json.loads(results)

    try:
        data = results['ask']['results']['items']
    except KeyError:
        raise ValueError("Bad API data")


    print HEADER

    for item in data:
        try:
            start_date = datetime.strptime(item['properties']['start_date'],
                                           "%Y-%m-%d %H:%M:%S"
                                           )
        except ValueError:
            # cannot parse date, move to next time
            continue

        try:
            uri = item['uri'][43:].encode("utf-8")
            url = googl.shorten(item['uri'][:43] +\
                                urllib.quote(uri)
                                ).encode("utf-8")

        except KeyError:
            url = ""

        calendar_entry = string.join(
            (
                "BEGIN:VEVENT",
                "UID:%s@hsgr" % item['title'].encode('utf-8').replace(' ', '_'),
                "DTSTAMP:%04d%02d%02dT%02d%02d00" % (start_date.year,
                                                     start_date.month,
                                                     start_date.day,
                                                     start_date.hour,
                                                     start_date.minute),
                "ORGANIZER;CN=Hackerspace:MAILTO:mail@hackerspace.gr",
                "DTSTART:%04d%02d%02dT%02d%02d00" % (start_date.year,
                                                     start_date.month,
                                                     start_date.day,
                                                     start_date.hour,
                                                     start_date.minute),

                "SUMMARY:%s" % unescape(item['title']).encode("utf-8"),
                "DESCRIPTION:%s" % (url),
                "END:VEVENT",
                ),
            "\r\n"
            )

        print calendar_entry

    print FOOTER

if __name__ == "__main__":
    main()
