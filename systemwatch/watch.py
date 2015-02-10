# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time

from . import plugins
from .common import memoize, entry_reader
from .config import Config
from .report import Report


class SystemWatch(object):

    def __init__(self, options):
        self.options = options

        Config.init(options)
        plugins.load()

    @memoize
    def reports(self):
        instances = {}

        def add_if_new(instance):
            name = instance.name
            if name and name not in instances:
                instances[name] = instance

        for instance in Report._instances:
            add_if_new(instance)

        classes = Report.subclasses()
        for c in classes:
            add_if_new(c())

        return instances

    def process(self, reports):
        for name, report in reports.items():
            for service in report.services:
                reader = entry_reader(service, report.log_level,
                                      time.time() - 900)
                result = report.process(reader)

            if result is False:
                reports.pop(name, None)

    def render(self, reports):
        template = Config().templates.report
        return ''.join(template.format(name=report.name,
                                       content=report.render())
                       for name, report in sorted(reports.items()))

    def run(self):
        reports = self.reports()
        self.process(reports)

        template = Config().templates.email
        output = template.format(title='Systemwatch',
                                 content=self.render(reports))

        return output
