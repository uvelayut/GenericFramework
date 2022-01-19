#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
     SubPage Class Implementation
"""

__author__ = "Biju Aramban"
__credits__ = ["Biju Aramban", ]
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Testing"
__date__ = '2019-08-16T20:49:05'


import time
from robot.api import logger
from libs.ui.AutoException import AutoException
from libs.util.CommonUtils import CommonUtils


class SubPage(object):
    """
    SubPage Class

    Used for any page inline operation.

    Parameters:
        :param selenium_session:
            - A valid selenium session. (Instance of ExtendedSeleniumLibrary)
    """

    def __init__(self, selenium_session, widget_locator=None, widget_name=None, expand=False):

        self.class_name = self.__class__.__name__
        logger.debug("%s | __init__ | Starting" % self.class_name)

        if not selenium_session:
            raise AutoException.NoSeleniumSessionException()

        self._selenium = selenium_session
        self.widget_locator = widget_locator
        self.widget_name = widget_name

        if (self.widget_locator or self.widget_name) and expand:
            self._expand_widget(widget_locator=self.widget_locator, widget_name=self.widget_name)

        return

    def _expand_widget(self, widget_locator, widget_name):

        logger.debug("%s | _expand_widget | Starting" % self.class_name)
        logger.debug(
            "%s | _expand_widget | Widget Locator: %s | Name: %s" % (
                self.class_name,
                repr(widget_locator),
                widget_name
            )
        )
        not_expanded = "glyphicon-angle-right"
        expanded = "glyphicon-angle-down"
        by = ""
        locator = self.widget_locator

        if widget_locator:
            if isinstance(widget_locator, (tuple, list)):
                by = widget_locator[0]
                locator = widget_locator[1]
            else:
                locator = widget_locator

        locator = widget_locator
        widget_element = None

        try:
            widget_element = self._selenium.find_element_extended(locator, widget_name)
        except Exception as e:
            logger.debug("_expand_widget | EXCEPTION | Details: %s" %  repr(e))

        if widget_element:
            logger.debug("_expand_widget | Widget found. Expanding Widget")
            self._selenium.click(self.widget_locator)
            self._selenium.wait_for_angular(timeout=10, track_ui_loading_time=False)

        else:
            error_message = "_expand_widget | Element not found | Locator: %s | Widget Name: %s" % (
                repr(locator),
                widget_name
            )
            logger.debug(error_message)
            logger.debug("_expand_widget | Assuming the Widget is EXPANDED. Continuing...")

        return

    def _set_widget_options(self, function_map, kwargs):

        logger.debug("%s | _set_widget_options | Starting" % self.class_name)
        logger.debug("kwargs | Type: %s | Args: %s" % (type(kwargs), repr(kwargs)))

        for item in kwargs.items():
            key, value = item
            function_map[key](value)

        time.sleep(0.5)
        return

    def checkbox_option(self, element, option):

        logger.debug("%s | checkbox_option | Starting" % self.class_name)
        enable = CommonUtils().validate_true_or_false(option)
        logger.debug("checkbox_option | Element: %s | Enable: %s" % (repr(element), enable))

        if enable:
            self._selenium.select_checkbox_ex(element)
        else:
            self._selenium.unselect_checkbox_ex(element)

        return

    def input_text(self, locator, text):

        logger.debug("%s | input_text | Starting" % self.class_name)
        if not text:
            text = ''

        logger.debug("%s | input_text | Text: %s | Locator: %s" % (self.class_name, text, repr(locator)))
        if text:
            self._selenium.send_keys(locator, text)
        else:
            self._selenium.clear(locator)

        return

    def is_card_expanded(self, card_element):

        logger.debug("%s | is_card_expanded | Starting" % self.class_name)
        expanded_flag = False
        card_web_element = self._selenium.find_elements(card_element)

        if card_web_element and isinstance(card_web_element, list):
            card_web_element = card_web_element[0]

        if card_web_element:
            try:
                card_expanded_scope = "glyphicon-angle-down"

                if card_expanded_scope in card_web_element.get_attribute("class"):
                    expanded_flag = True

            except Exception as excp:
                logger.debug("is_card_expanded | EXCEPTION | Details: %s" % repr(excp))

        return expanded_flag

    def set_options(self, function_map, kwargs, card=None):

        logger.debug("%s | set_options | Starting" % self.class_name)
        # if card:
        #     logger.debug("set_options | Expanding Card | Card: %s" % card)
        #     self._expand_widget(widget_locator=None, widget_name=card)

        return self._set_widget_options(function_map, kwargs)

    def validate_parameters_kwargs(self, expected, actual):

        logger.debug("%s | validate_parameters_kwargs | Starting" % self.class_name)
        if not isinstance(expected, (tuple, list)):
            logger.debug("validate_parameters_kwargs | Expected: %s" % repr(expected))
            raise AutoException.InvalidTypeException(type(list), type(expected))

        if not isinstance(actual, dict):
            logger.debug("validate_parameters_kwargs | Actual: %s" % repr(actual))
            raise AutoException.InvalidTypeException(type(actual), type(actual))

        diff_list = list(set(actual.keys()) - set(expected))
        if diff_list:
            logger.error("Invalid Parameters | Invalid parameters passed: %s" % ', '.join(diff_list))
            logger.info("Valid Parameters this method can take are: %s" % ', '.join(expected))
            raise AutoException.InvalidParameterException(diff_list)

        return


class SubPageCheckBox(SubPage):

    def __init__(self, selenium_session):
        super(SubPageCheckBox, self).__init__(selenium_session)
        return

    def set_checkbox_option(self, option_string=None, checkbox_identifier=None, checkbox_locator=None):

        logger.debug("%s | set_checkbox_option | Starting" % self.class_name)
        logger.debug(
            "set_checkbox_option | option_string: %s | checkbox_identifier: %s | checkbox_locator: %s" % (
                option_string,
                checkbox_identifier,
                checkbox_locator
            )
        )
        if not checkbox_identifier or not option_string or not checkbox_locator:
            raise AutoException.IncompleteDataException(
                "Missing Mandatory Parameter(s)\n"
                "Madatory Parameters:\n"
                "    - option_string - String in the format: key=value\n"
                "    - checkbox_identifier - String\n"
                "    - checkbox_locator - Tuple in the format (By.Type, Locator_string)\n"
            )

        if option_string:
            option_dict = CommonUtils().convert_to_dictionary(option_string)
            if not option_dict or checkbox_identifier not in option_dict:
                logger.debug("set_checkbox_option | Missing checkbox_identifier Key: %s" % checkbox_identifier)
                raise AutoException.InvalidParameterException(option_dict.keys())

            self.checkbox_option(checkbox_locator, option_dict[checkbox_identifier])
        return
