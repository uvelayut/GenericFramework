#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
     SingletonBrowser Class Implementation
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
from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary.base import keyword

from libs.ui.Constants import Constants
from libs.ui.ExtendedSeleniumLibrary import *
from libs.ui.constants_browsers_drivers import BROWSERS


class InvalidBrowser(BaseException):
    pass


class SingletonBrowser():
    """
        SingletonBrowser
        For any given dut and browser combination, create only once class instance so that it is bound to
        the same selenium and browser.

        At any given point there will only be a single active browser.
        If you want to switch, you have to call 'Set Active Browser'
    """

    ROBOT_LIBRARY_SCOPE = 'TEST CASE'

    _dut_browser_instances = {}
    _active_browser = None

    def __init__(self, dut, browser=BROWSERS.CHROME, server='localhost', port=4444):
        self.dut = dut
        self.browser = browser
        self.server = server
        self.port = port
        self.default_browser = BROWSERS.CHROME

        if not browser:
            browser = self.default_browser

        BuiltIn().log("Browsers: %s | Current Browser: %s\n" % (Constants.get_constant_values(BROWSERS), browser))

        if browser not in Constants.get_constant_values(BROWSERS):
            raise InvalidBrowser("Unsupported Browser | Browser: %s" % browser)

        BuiltIn().log("DUT: %s | Browser: %s | Server: %s | Port: %s\n" % (
            self.dut, self.browser, self.server, self.port
            )
        )
        BuiltIn().log("Browser Instances: %s\n" % self._dut_browser_instances)

        if dut not in self._dut_browser_instances:
            self._dut_browser_instances[dut] = {browser: ExtendedSeleniumLibrary()}  # dut, browser, server, port)}
        elif browser not in self._dut_browser_instances[dut]:
            self._dut_browser_instances[dut].update({browser: ExtendedSeleniumLibrary()})  # dut, browser, server, port)})

        #self.set_active_browser_session(dut, browser)
        SingletonBrowser._active_browser = SingletonBrowser._dut_browser_instances[dut][browser]

        #return self._dut_browser_instances[dut][browser]

        super().__init__()
        return

    @classmethod
    @keyword(name="Set Active Browser Session")
    def set_active_browser_session(cls, dut, browser=BROWSERS.FIREFOX):
        if dut in cls._dut_browser_instances and browser in cls._dut_browser_instances[dut]:
            cls._active_browser = cls._dut_browser_instances[dut][browser]
        print("Active Browser: %s" % cls._active_browser)
        return cls._active_browser

    @classmethod
    @keyword(name="Get Active Browser Session")
    def get_active_browser_session(cls, dut=None, browser=BROWSERS.FIREFOX):

        if not dut:
            dut = os.getenv("DUT", None)

        if not dut:
            raise AutoException("DUT Environment variable not set OR DUT is not passed as an argument.")

        if not cls._active_browser:
            print(
                "No Active Browser | Active Browser: %s | Code will now set the Active Browser." % cls._active_browser
            )
            cls.set_active_browser_session(dut, browser)

        print("Active Browser Set: %s" % cls._active_browser)
        return cls._active_browser


    def __getattr__(self, name):

        #logger.info("Address: %s | Object: %s | Function: %s" %(self.gui, type(self.gui), name))

        if name == '_active_browser':
            raise RuntimeError('GUI has not been initialized')

        return getattr(SingletonBrowser._active_browser, name)

# ---------------------------------------------------------------------------------------------------------------- #
# Unit Test Code
# ---------------------------------------------------------------------------------------------------------------- #
class TestSingleton(SingletonBrowser):

    def __init__(self, dut=None, browser=BROWSERS.FIREFOX, server='localhost', port=4000):
        super().__init__(dut, browser, server, port)
        print(super().__dict__)
        return


def test_singleton():

    a = TestSingleton(dut='a', browser=BROWSERS.FIREFOX, server='localhost', port=4000)
    b = TestSingleton(dut='b', browser=BROWSERS.FIREFOX, server='localhost', port=4000)
    print(
        "a: %s | dut: %s | browser: %s | server: %s | port: %d" % (a, a.dut, a.browser, a.server, a.port),
        "\nb: %s | dut: %s | browser: %s | server: %s | port: %d" % (b, b.dut, b.browser, b.server, b.port)
    )
    assert a is not b, "a is b. It should not have been."
    a.open_browser('https://google.com/', BROWSERS.FIREFOX)

    c = TestSingleton(dut='a', browser=BROWSERS.INTERNET_EXPLORER, server='localhost', port=4000)
    d = TestSingleton(dut='d', browser=BROWSERS.FIREFOX, server='localhost', port=4000)
    print(
        "c: %s | dut: %s | browser: %s | server: %s | port: %d" % (c, c.dut, c.browser, c.server, c.port),
        "\nd: %s | dut: %s | browser: %s | server: %s | port: %d" % (d, d.dut, d.browser, d.server, d.port)
    )
    assert a is not c, "a is c. It should not have been."

    c = TestSingleton(dut='a', browser=BROWSERS.FIREFOX, server='localhost', port=4000)
    d = TestSingleton(dut='b', browser=BROWSERS.FIREFOX, server='localhost', port=4000)
    print(
        "c: %s | dut: %s | browser: %s | server: %s | port: %d" % (c, c.dut, c.browser, c.server, c.port),
        "\nd: %s | dut: %s | browser: %s | server: %s | port: %d" % (d, d.dut, d.browser, d.server, d.port)
    )
    assert a is c, "a is not c. It should have been."
    try:
        d = TestSingleton(dut='b', browser="ie", server='localhost', port=4000)
        print(
            "d: %s | dut: %s | browser: %s | server: %s | port: %d" % (d, d.dut, d.browser, d.server, d.port)
        )
    except InvalidBrowser as inv_browser:
        print("EXCEPTION | Details: %s" % inv_browser)

    SingletonBrowser.set_active_browser_session(a.dut, a.browser)
    SingletonBrowser.set_active_browser_session(b.dut, b.browser)
    SingletonBrowser.get_active_browser_session(a.dut, a.browser)

    a.open_web_browser('google.com', BROWSERS.FIREFOX)

    return


if __name__ == '__main__':
    test_singleton()
