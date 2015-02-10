# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from systemd import journal
from ..report import MultisectionReport, RegexGrouping


ZNC = MultisectionReport(
    name='ZNC',
    services=[
        'znc.service',
    ],
    log_level=journal.LOG_DEBUG,
    sections=[
        RegexGrouping(
            name='Modpython Errors',
            patterns=[
                r'modpython: (?P<function>\w+(?:[\/\w]+)*): (?P<error>.+) '
                '(?P<traceback>Traceback .+)?',
            ],
        )
    ],
)
