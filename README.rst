tramtracker
===========

This provides a python wrapper for Yarra Trams' Tram Tracker data,
accessed via tramtracker.com. Given a stop id and optionally a tram
route number, returns the minutes to wait for the next tram.

Installation
------------
Grab the file tramtracker.py and execute it, or:

::

   pip install tramtracker

Or, you can download the source and

::

   python setup.py install

or

::

    sudo python setup.py install

if required.

Command-Line Usage
------------------

In your command-line, invoke with a stop id and optionally a route:

::

    $ tramtracker.py 3110

    Next trams:
    72:  8 minutes
     1: 10 minutes
     4:  0 minutes
    16:  9 minutes
     8: 13 minutes

From Python
-----------
::

    >>> import tramtracker
    >>> my_tram = 1
    >>> my_stop = 3110
    >>> mins_to_wait = tramtracker.get_next_time(my_stop, my_tram)
    >>> mins_to_wait
    4.823830298582712
    >>> tramtracker.get_next_times(my_stop)
    {72: 2.564150317509969, 1: 4.964150631427765, ...}

