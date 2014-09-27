#!/usr/bin/python
# tramtracker
# -*- coding: latin-1 -*-
# ----------------------------------------------------------------------------
# I, Colin Jacobs, <colin@coljac.net>, the author of this file, release it
# to the public domain for use and modification without restriction. Where
# possible, retaining acknowledgement of original authorship is appreciated.
# ----------------------------------------------------------------------------
# ****************************************************************************
# * Software: tramtracker                                                    *
# * Version:  0.1                                                            *
# * Date:     2014-09-26                                                     *
# * Last update: 2014-09-26                                                  *
# *                                                                          *
# * Author:  Colin Jacobs, colin@coljac.net                                  *
# *                                                                          *
# * A wrapper for Yarra Trams' Tram Tracker data, accessed via               *
# * tramtracker.com.                                                         *
# *                                                                          *
# * If you don't live in Melbourne, Australia, this is probably not the      *
# * module you're looking for.                                               *
# *                                                                          *
# * Usage from command line:                                                 *
# *                                                                          *
# *     tramtracker.py  stopID [route]                                       *
# *                                                                          *
# *     $ python tramtracker.py 3110                                         *
# *     Next trams:                                                          *
# *     72: 1 minutes                                                        *
# *      1: 2 minutes                                                        *
# *      ...                                                                 *
# *                                                                          *
# * Usage from python:                                                       *
# *                                                                          *
# *     >>> import tramtracker                                               *
# *     >>> my_tram = 1                                                      *
# *     >>> my_stop = 3110                                                   *
# *     >>> mins_to_wait = tramtracker.get_next_time(my_stop, my_tram)       *
# *     >>> mins_to_wait                                                     *
# *     4.823830298582712                                                    *
# *     >>> tramtracker.get_next_times(my_stop)                              *
# *     {72: 2.564150317509969, 1: 4.964150631427765, ...}                   *
# ****************************************************************************
import json, re, time

TT_URL = "http://www.tramtracker.com/Controllers/GetNextPredictionsForStop.ashx"

def _call_tt(stop=1421, route=19):
    import urllib
    page = urllib.urlopen(TT_URL +
                    "?stopNo=%s&routeNo=%s&isLowFloor=false" % (stop, route))
    return page.read()

def _get_minutes_from_date_string(time_string):
    time_string = re.match(r'.*(\d{13}).*',
                str(time_string)).group(1)
    seconds_until_tram = int(time_string)/1000. - time.time()
    return (seconds_until_tram/60)

def get_next_time(stop=1421, route=19):
    """
    :param stop: The id of the tram stop. Can be found in the apps or Yarra
     Trams website.
    :param route: The tram route/line number.
    :return: the time, in minutes, until the next tram at the stop.
    """
    raw_result = _call_tt(stop, route)
    json_obj = json.loads(raw_result)
    next_string = json_obj['responseObject'][0]['PredictedArrivalDateTime']
    return _get_minutes_from_date_string(next_string)

def get_next_times(stop):
    """
    :param stop: The id of the tram stop. Can be found in the apps or Yarra
     Trams website.
    :return: A dict, containing the tram ids as keys and the the time,
    in minutes, until the next tram of that route as the values.

    e.g. {'1': '12.3', '8': '2.5'}
    """
    raw_result = _call_tt(stop, 0)
    json_obj = json.loads(raw_result)['responseObject']
    trams = {}
    for resp in json_obj:
        tram = resp['InternalRouteNo']
        time = _get_minutes_from_date_string(resp['PredictedArrivalDateTime'])
        if trams.has_key(tram):
            if trams[tram] > time:
                trams[tram] = time
        else:
            trams[tram] = time
    return trams

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Get the time to the next '
                                                 'tram from TramTracker, '
                                                 'courtesy of Yarra Trams.\n\n'
                                                 'For more information: '
                                                 'http://yarratrams.com.au\n\n'
                                                 'Usage: soapytracker.py stop [route]')
    parser.add_argument('stopID', metavar='stopID', type=int,
                   help='the stop id (see web or official app)')
    parser.add_argument('route', metavar='route', type=int, nargs='?',
                   help='the tram route number')
    parser.add_argument('-q', '--quiet', help='print raw time only',
                   default=False, action='store_true')


    args = parser.parse_args()

    if(args.route):
        mins = get_next_time(args.stopID, args.route)
        if(args.quiet):
            print "%.1f" % mins
        else:
            print("Next %d tram in %d minutes." % (args.route, mins))
    else:
        times = get_next_times(args.stopID)
        if not args.quiet:
            print("Next trams: ")
        for tram, minutes in times.iteritems():
            if args.quiet:
                print("%d: %d" % (tram, minutes))
            else:
                print(" %2d: %2d minutes" % (tram, minutes))
