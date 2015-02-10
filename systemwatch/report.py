# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from collections import Counter, defaultdict
from ent import Ent

from .common import memoize
from .config import Config


class Report(Ent):
    '''
    This class provides the framework for generating reports from the systemd
    journal over a given period of time.  The output of the report is
    plaintext with Markdown formatting.
    '''

    name = None
    services = {}

    def process(self, reader):
        return False

    def render(self):
        return ''

    # internal implementation

    _instances = None

    def __init__(self, *args, **kwargs):
        super(Report, self).__init__(*args, **kwargs)

        if Report._instances is None:
            Report._instances = []

        Report._instances.append(self)

    @classmethod
    def instances(cls):
        if Report._instances is None:
            return []

        return Report._instances


class Section(Ent):

    name = None

    def process(self, reader):
        return False

    def render(self):
        return ''


class RegexGrouping(Section):
    '''
    This class provides a simple mechanism for matching a set of regular
    expressions, and aggregating the resulting values for later retrieval.
    '''

    patterns = None

    def process(self, reader):
        if not self.patterns:
            return False

        self.matches = set()
        self.match_counter = Counter()
        self.values = defaultdict(set)

        for entry in reader:
            for pattern in self._compiled_patterns():
                match = pattern.search(entry.message)
                if match:
                    whole_match = match.group(0)
                    self.matches.add(whole_match)
                    self.match_counter[whole_match] += 1

                    for pos, value in enumerate(match.groups()):
                        self.values[pos].add(value)
                        # self.counters[pos][value] += 1

                    for key, value in match.groupdict().items():
                        self.values[key].add(value)
                        # self.counters[key][value] += 1

                    break  # only care about the first regex to match a line

    def render(self):
        return '{}'.format(self.match_counter)

    @memoize
    def _compiled_patterns(self):
        result = []

        if self.patterns is None:
            return result

        for pattern in self.patterns:
            result.append(re.compile(pattern))

        return result


class MultisectionReport(Report):

    sections = None

    def process(self, reader):
        if not self.sections:
            return False

        for section in self.sections:
            section.process(reader)

    def render(self):
        template = Config().templates.section
        return ''.join(template.format(name=section.name,
                                       content=section.render())
                       for section in self.sections)
