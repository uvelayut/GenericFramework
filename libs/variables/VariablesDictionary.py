#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
     VariablesDictionary Class Implementation

    That modules is a simple wrapper for Robot's BuiltIn variable methods
    If used from Robot, it returns all Robot's variables
    If used outside of Robot, it allows setting and getting global variables

    Usage:
    import ui.variables.VariablesDictionary
    ...
    variables = VariablesDictionary.get_global_variables_dictionary()

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


import os
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.variables import variables
from libs.ui.Singleton import Singleton
from libs.ui.constants_browsers_drivers import BROWSERS


DUT = os.getenv('DUT', "")

"""
Local Variables Dictionary holds the mandatory Variables and their DEFAULT values.
These values will update the BuiltIn().Variables() in Global Object
"""
local_variables_dictionary = {
    "${DUT}": DUT,
    "${DUT_ADMIN}": "admin",
    "${DUT_ADMIN_PASSWORD}": "password",
    "${BROWSER}": BROWSERS.CHROME,
    "${SERVER}": 'localhost',
    "${PORT}": 4444,
    "${PAGE_LOAD_TIME}": {},
}


class VariablesDictionary(object, metaclass=Singleton):
    """
    VariablesDictionary
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):

        self.built_in = BuiltIn()
        self.builtin_variables = self.built_in.get_variables()

        for key in local_variables_dictionary:
            if key not in self.builtin_variables:
                self.builtin_variables[key] = local_variables_dictionary[key]
        return

    def _get_global_variable_name(self, variable_name):
        """

        """
        global_var = ''
        if variable_name:
            global_var = str(variable_name).strip()

            if not global_var.startswith("${"):
                global_var = "${%s" % global_var

            if not global_var.endswith("}"):
                global_var = "%s}" % global_var

        return global_var

    def _update_global_variable_dict(self, variable_name, value):
        """
        _update_global_variable_dict
            Sets a global variable.

        Parameters:
            :param variable_name:
                - name of the variable name
            :param value:
                - value of the variable to update.
        Returns: NIL

        self._update_global_variable_dict("variable_name", {1: 2,})
        """
        global_var = self._get_global_variable_name(variable_name)
        variable_value = self.get_global_variable(global_var)

        if not variable_value or not isinstance(variable_value, dict):
            self.set_global_variable(variable_name, value)
        elif isinstance(variable_value, dict):
            variable_value.update(value)
            local_variables_dictionary[global_var].update(value)

        return

    def _update_global_variable_tuple(self, variable_name, value):
        """
        _update_global_variable_tuple
            Sets a global variable.

        Parameters:
            :param variable_name:
                - name of the variable name
            :param value:
                - value of the variable to update.
        Returns: NIL

        self._update_global_variable_tuple("variable_name", (1, 2, 3,))
        """
        global_var = self._get_global_variable_name(variable_name)
        variable_value = self.get_global_variable(global_var)

        if not variable_value or not isinstance(variable_value, tuple):
            self.set_global_variable(variable_name, value)
        elif isinstance(variable_value, tuple):
            variable_value = list(variable_value)
            variable_value.extend(value)
            self.set_global_variable(variable_name, variable_value)

        return

    def _update_global_variable_list(self, variable_name, value):
        """
        _update_global_variable_list
            Sets a global variable.

        Parameters:
            :param variable_name:
                - name of the variable name
            :param value:
                - value of the variable to update.
        Returns: NIL

        self._update_global_variable_list("variable_name", [1, 2, 3,])
        """
        global_var = self._get_global_variable_name(variable_name)
        variable_value = self.get_global_variable(global_var)

        if not variable_value or not isinstance(variable_value, list):
            self.set_global_variable(variable_name, value)
        elif isinstance(variable_value, list):
            variable_value.extend(value)
            self.set_global_variable(variable_name, variable_value)

        return

    def _update_global_variable_scalar(self, variable_name, value):
        """
        _update_global_variable_scalar
            Update a scalar value

        Parameters:
            :param variable_name:
                - name of the variable name
            :param value:
                - value of the variable to update.

        Returns: NIL
        self._update_global_variable_scalar("variable_name", "some_value")
        """
        self.set_global_variable(variable_name, value)
        return

    def dut(self):
        """
        dut
            Returns the dut variable from the dictionary

        Parameters: NIL
        Returns:
            dut name
        """
        return local_variables_dictionary['${DUT}']

    def delete_variable(self, key):
        if key in local_variables_dictionary:
            del local_variables_dictionary[key]
        else:
            logger.debug("Invalid Key | Key: %s" % key)

    def get_global_variable(self, variable_name):
        try:
            self.builtin_variables.update(local_variables_dictionary)
            global_var = self._get_global_variable_name(variable_name)
            return self.get_global_variables_dictionary().get(global_var)
        except:
            return None

    def set_global_variable(self, variable_name, value):
        """
        set_global_variable
            Sets a global variable.
            This will be available in Global object

        Parameters:
            :param variable_name:
                - name of the variable name
            :param value:
                - value of the variable to update.

        Returns: NIL
        """
        global_var = self._get_global_variable_name(variable_name)
        self.built_in.set_global_variable(global_var, value)
        local_variables_dictionary[global_var] = value

    def update_global_variable(self, variable_name, value):
        """
        set_global_variable
            Sets a global variable.

        Parameters:
            :param variable_name:
                - name of the variable name
            :param value:
                - value of the variable to update.

        Returns: NIL
        self.update_global_variable("some_variable", "some_value")
        """
        global_var = self._get_global_variable_name(variable_name)

        if isinstance(value, dict):
            self._update_global_variable_dict(global_var, value)
        elif isinstance(value, tuple):
            self._update_global_variable_tuple(global_var, value)
        elif isinstance(value, list):
            self._update_global_variable_list(global_var, value)
        else:
            self._update_global_variable_scalar(global_var, value)

        return

    def get_global_variables_dictionary(self):
        """
        get_global_variables_dictionary

            Parameters: NIL
            Returns: Global Variables Dictionary with merged values from the Local Variables Dictionary
        """
        try:
            if not self.builtin_variables:
                self.builtin_variables = self.built_in.get_variables()   # BuiltIn().get_variables()
            self.builtin_variables.update(local_variables_dictionary)

            return self.builtin_variables
        except:
            return None

    def update(self, update_dict):
        """
        update
            Update the Global Variables Dictionary with user dictionary
            Makes the user created variables available across functions
            SCOPE: Test Suite

        Parameters:
        :param update_dict: The user dictionary which has to be updated with the Global
            variables dictionary

        Returns: NIL
        """
        if update_dict and isinstance(update_dict, dict):
            for key, value in update_dict:
                self.builtin_variables[key] = value
