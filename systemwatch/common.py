# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from ent import Ent
from functools import wraps
from future.builtins import bytes
from systemd import journal


class Entry(Ent):
    message = ''
    unit = ''
    time = 0
    priority = journal.LOG_INFO


def memoize(fn):
    '''Cache the results of a function that only takes positional arguments.'''

    cache = {}

    @wraps(fn)
    def wrapped_function(*args):
        if args in cache:
            return cache[args]

        else:
            result = fn(*args)
            cache[args] = result
            return result

    return wrapped_function


def entry_reader(service, loglevel, start_time):
    with journal.Reader() as reader:
        reader.seek_realtime(datetime(2015, 2, 8, 0, 0, 0))
        reader.get_next()

        reader.add_match(_SYSTEMD_UNIT=service)
        reader.log_level(loglevel)

        for entry in reader:
            msg = entry['MESSAGE']
            dt = entry['__REALTIME_TIMESTAMP']

            if isinstance(msg, bytes):
                try:
                    msg = msg.decode('utf-8')
                except UnicodeError:
                    continue

            yield Entry(message=msg,
                        datetime=dt,
                        unit=entry['_SYSTEMD_UNIT'],
                        priority=entry['PRIORITY'],
                        )
