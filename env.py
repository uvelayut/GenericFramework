#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
     env - Environment Settings
"""

__author__ = "Udhandaraman Velayutham"
__credits__ = ["Biju Aramban", "Udhandaraman Velayutham"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = ""
__email__ = ""
__status__ = "Testing"
__date__ = '2021-08-10T20:49:05'


import os
from libs.variables.defaults import DEFAULTS
from robot.api import logger

HOME = os.getenv(DEFAULTS.HOME, '')

if not HOME:
    CWD = os.path.dirname(os.path.realpath(__file__))
    AUTO_HOME = os.path.dirname(os.path.dirname(CWD))
    os.environ[DEFAULTS.HOME] = HOME

LIB_PATH= "%s/libs" % HOME
os.environ[DEFAULTS.PYTHONPATH] = LIB_PATH

logger.info("HOME: %s | PYTHONPATH=LIB_PATH: %s" % (
    HOME,
    LIB_PATH
    )
)
