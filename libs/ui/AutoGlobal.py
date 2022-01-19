#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
     Global Class Implementation
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


from libs.variables.VariablesDictionary import VariablesDictionary


class AutoGlobal(object):
    """
        AutoGlobal
            Class sets up the run environment for the tests.
            Internal Class used by all the GUI classes
            It can cross reference the BuiltIn Variables and it can set variables in the runtime.
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(
            self,
            config_file=None
    ):
        self.config_file = config_file
        self.config = None
        self.global_variables = VariablesDictionary()

        if self.config_file:
            self.config = self.parse_config()

    def get_global_variables_dictionary(self):
        return self.global_variables

    def get_global_variable(self, variable_name):
        return self.global_variables.get_global_variable(variable_name)

    def set_global_variable(self, variable_name, value):
        return self.global_variables.set_global_variable(variable_name, value)

    def parse_config(self, config_file=None):

        if not config_file:
            config_file = self.config_file

        if not config_file:
            return

        self.config = None

    def update_variables(self):

        if self.config:
            if isinstance(self.config, type({})):
                self.global_variables.update(self.config)
