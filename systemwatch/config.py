# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from os import path

from ent import Ent, json


class Config(Ent):

    _instance = None

    def __repr__(self):
        return '<Config>'

    def __new__(cls, *args, **kwargs):
        if Config._instance is None:
            return super(Config, cls).__new__(cls)

        return Config._instance

    def __init__(self, *args, **kwargs):
        if Config._instance is None:
            super(Config, self).__init__(*args, **kwargs)

    @classmethod
    def init(cls, options):
        defaults_path = path.join(path.dirname(__file__), 'defaults.json')

        with open(defaults_path) as f:
            defaults = json.load(f)
            config = Config.load(defaults, promote=True)

        Config._instance = config
