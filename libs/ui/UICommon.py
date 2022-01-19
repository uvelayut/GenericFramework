#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
     UICommon Class Implementation
"""

__author__ = "Biju Aramban"
__copyright__ = "Copyright 2020"
__credits__ = ["Biju Aramban", ]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = ""
__email__ = ""
__status__ = "Testing"
__date__ = '2019-08-16T20:49:05'


from robot.libraries.BuiltIn import BuiltIn
from libs.ui.AutoGlobal import AutoGlobal


class UICommon(object):
    """
    UICommon
        - Holds the UI Initialization Specific Variables
        - Holds the Global Object
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):

        self.global_object = AutoGlobal()
        BuiltIn().log("Global Object: %s | Dir: %s" % (self.global_object, dir(self.global_object)))
        self.dut = self.global_object.get_global_variable("PORTAL")
        self.browser = self.global_object.get_global_variable("BROWSER")
        self.server = self.global_object.get_global_variable("SERVER")
        self.port = self.global_object.get_global_variable("PORT")

        return
