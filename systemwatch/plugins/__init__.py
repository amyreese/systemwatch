# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import importlib
import os
from os import path

cwd = path.abspath(path.dirname(__file__))
files = os.listdir(cwd)


def load():
    for filename in files:
        name, ext = path.splitext(filename)

        if name.startswith('_'):
            continue

        if ext == '.py':
            importlib.import_module('systemwatch.plugins.' + name)
