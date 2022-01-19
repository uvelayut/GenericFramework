from robot.api import logger


class AutoException(BaseException):
    """ Extended SeleniumLibrary is a web testing GUI library for Robot Framework.
            Library contains all Robot Selenium keywords that are customised on top of the existing Selenium
            keywords. Extended SeleniumLibrary uses the Selenium Library modules internally to
            control a web browser.

            For more details on Selenium Library - Please visit
            "https://github.com/robotframework/SeleniumLibrary"

            To write methods/keywords in the python modules for Robot Framework, SeleniumEx must be
            imported into your basepage which in turn will inherited by other GUI python modules.

        """
    pass


class AssertionErrorException(AutoException):
    """Raised when assertion fails"""
    def __init__(self, expected_text, e):
        logger.error(
            "%s | Assertion Error - Text not found | Expected Text: %s\nDetails: %s" %
            (__class__.__name__, expected_text, e)
        )


class BrowserPageNotLoadedException(AutoException):
    """Raised when the browser is not opened"""
    def __init__(self, e):
        logger.error("%s | Browser page not loaded.\nEXCEPTION DETAILS:\n%s" % (__class__.__name__, e))


class ElementClickInterceptedException(AutoException):
    """Raised when element click is not working"""
    def __init__(self, ui_element):
        logger.error("%s | Element Click was intercepted | Element: %s" % (__class__.__name__, ui_element))


class IncompleteDataException(AutoException):
    """Raised when the data a function expects is incomplete"""
    def __init__(self, message):
        logger.error("%s | Details: %s" % (__class__.__name__, message))


class InvalidInputException(AutoException):
    """Raised when the element is not visible or unavailable"""
    def __init__(self, invalid_input):
        if not isinstance(invalid_input, list):
            invalid_input = [repr(invalid_input), ]

        logger.error("%s | Invalid Input: %s" % (__class__.__name__, ", ".join(invalid_input)))


class InvalidParameterException(AutoException):
    """Raised when the element is not visible or unavailable"""
    def __init__(self, invalid_params):
        if not isinstance(invalid_params, list):
            invalid_params = [invalid_params, ]

        logger.error("%s | Unexpected Parameters: %s" % (__class__.__name__, ", ".join(invalid_params)))


class InvalidReportException(AutoException):
    """Raised when the element is not visible or unavailable"""
    def __init__(self, report_name):
        logger.error("%s | Report Not Found | Report: %s" % (__class__.__name__, report_name))


class InvalidTabException(AutoException):
    """Raised when the element is not visible or unavailable"""
    def __init__(self, tab_name):
        logger.error("%s | Tab Not Found | Tab: %s" % (__class__.__name__, tab_name))


class InvalidOptionError(AutoException):
    """Raised when the dropdown option is not a valid one"""
    def __init__(self, e):
        logger.error("%s | Please check the option passed.\nEXCEPTION DETAILS:\n%s" % (__class__.__name__, e))


class InvalidTypeException(AutoException):
    """Raised when the element is not visible or unavailable"""
    def __init__(self, expected_type, actual_type):
        logger.error(
            "%s | The data type is unexpected | Expected Type: %s | Actual Type: %s" %
            (
                __class__.__name__,
                expected_type,
                actual_type
            )
        )


class KeyErrorException(AutoException):
    """ Raised when key value is not returned"""
    def __init__(self, key):
        logger.error("%s | Key not found | Key: %s" % (__class__.__name__, repr(key)))


class NameErrorException(AutoException):
    """ Raised when there is an error in the object name accessed."""

    def __init__(self, key):
        logger.error("%s | Name not found | Key: %s" % (__class__.__name__, repr(key)))


class NoSeleniumSessionException(AutoException):
    """Raised when the selenium session is invalid"""

    def __init__(self):
        logger.error("%s | Selenium Session is not set." % __class__.__name__)


class TableNotFoundException(AutoException):
    """Raised when the table that is looking for is not found"""
    def __init__(self, element):
        logger.error("%s | Element: %s" % (__class__.__name__, repr(element)))


class TimeOutException(AutoException):
    """Raised when the time specified for an action is excceded"""
    def __init__(self, timeout, e):
        logger.error("%s | Timeout Error | Waited for: %s\nEXCEPTION DETAILS:\n%s" % (__class__.__name__, timeout, e))
