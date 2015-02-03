#!/usr/bin/python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import sys

try:
    import systemd
    from systemd import journal

except ImportError:
    print('Error: could not import systemd')
    sys.exit(1)


reader = journal.Reader()
reader.this_boot()
reader.log_level(journal.LOG_INFO)
reader.add_match(_SYSTEMD_UNIT="znc.service")

modpython_re = re.compile(r'modpython')

for entry in reader:
    message = entry['MESSAGE']

    if isinstance(message, bytes):
        try:
            message = message.decode('utf-8')
        except:
            print('decode fail')
            print(message)
            continue

    match = modpython_re.search(message)
    if match:
        pass
        #print('{_SYSTEMD_UNIT}: {PRIORITY} {__REALTIME_TIMESTAMP} {MESSAGE}'.format(**entry))
