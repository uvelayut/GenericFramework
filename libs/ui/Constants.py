#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
     Constants Class Implementation
"""

__author__ = "Biju Aramban"
__credits__ = ["Biju Aramban", ]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Testing"
__date__ = '2019-08-16T20:49:05'

import sys


class ConstantDefineInUpperError(BaseException):
    pass


class ConstantRebindError(BaseException):
    pass


class ConstantDoesNotExist(BaseException):
    pass


class Constants:

    def __init__(self):
        pass

    def __setattr__(self, name, value):

        if not (isinstance(name, str) and name.isupper()):
            raise ConstantDefineInUpperError(
                "Please define the constants_string_table in UPPER_CASE | Constant name: %s" % name
            )

        if name in self.__dict__:
            raise(
                ConstantRebindError(
                    "Cannot rebind a constant. Constant Name: {} | Current Value: {} | New Value: {}".format(
                        name,
                        self.__dict__[name],
                        value
                    )
                )
            )
        self.__dict__[name] = value

    def __getattr__(self, name):
        if name not in self.__dict__:
            raise(
                ConstantDoesNotExist(
                    "Constant not created. Constant Name: {const_name}".format(const_name=name)
                )
            )
        return self.__dict__[name]

    def __iter__(self):
        return iter(self.__dict__.items())

    def get_variables(self):
        return self.__dict__.items()

    def get_values(self):
        return self.__dict__.values()

    def get_key(self, value):

        value = str(value).lower()

        for key, key_value in self.__iter__():
            if value == str(key_value).lower():
                return key

        return None

    @classmethod
    def get_value(cls, key):

        key = str(key).upper()

        for const_key, key_value in iter(cls.__dict__.items()):
            if const_key == str(key):
                return key_value

        return None

    @staticmethod
    def get_constant_values(t_const):
        values = [value[1] for value in t_const.__dict__.items() if isinstance(value[0], str) and value[0].isupper()]
        return values

    @staticmethod
    def get_constant_key(t_const, value):
        keys = [key for key, key_value in t_const.__dict__.items() if value == key_value]
        return keys

    @staticmethod
    def get_key_lookup(t_const):

        keys = [
            str(value[1]).strip().lower().replace(" ", "_") for value in t_const.__dict__.items() if
                      isinstance(value[0], str) and value[0].isupper()
        ]
        constant_strings = Constants.get_constant_values(t_const)
        lookup_strings = dict(zip(keys, constant_strings))

        return lookup_strings

# ---------------------------------------------------------------------------------------------------------------- #
# Unit Test Code
# ---------------------------------------------------------------------------------------------------------------- #
def test_constant():
    """
        Constants Testing Code
        :return: None
    """

    CONST_TEST = Constants()

    sys.stdout.write("Test: Set Constant\n")
    CONST_TEST.TEST1 = "Value1 for Test1"
    sys.stdout.write('CONST_TEST.Test: %s\n' % CONST_TEST.TEST1)

    try:
        sys.stdout.write("Test: Rebind Constant\n")
        CONST_TEST.TEST1 = "Value1 for Test1"
    except ConstantRebindError as cre:
        sys.stdout.write('Exception (ConstantRebindError): %s\n' % repr(cre))

    try:
        sys.stdout.write("Test: Non Existent Constant\n")
        sys.stdout.write("CONST_TEST.TEST2 = %s\n" % CONST_TEST.TEST2)
    except ConstantDoesNotExist as cde:
        sys.stdout.write('Exception (ConstantDoesNotExist): %s\n' % repr(cde))

    try:
        sys.stdout.write("Test: Lower case Constant\n")
        CONST_TEST.Test2 = 1
    except ConstantDefineInUpperError as cde:
        sys.stdout.write('Exception (ConstantDefineInUpperError): %s\n' % repr(cde))

    sys.stdout.write("Variables:\n==========\n{}\n".format(CONST_TEST.get_variables()))

    for item in CONST_TEST:
        print(item)

    print(Constants.get_values(CONST_TEST))
    print(Constants.get_key_lookup(CONST_TEST))


if __name__ == '__main__':
    sys.exit(test_constant())
