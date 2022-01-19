import time
from SeleniumLibrary import ScreenshotKeywords
from selenium.common.exceptions import WebDriverException
from SeleniumLibrary import SeleniumLibrary, WaitingKeywords, AlertKeywords, CookieKeywords, FormElementKeywords, \
    ElementKeywords, FrameKeywords, JavaScriptKeywords, SelectElementKeywords, TableElementKeywords, WindowKeywords, \
    ElementFinder
from SeleniumLibrary.base import keyword
from SeleniumLibrary.keywords import BrowserManagementKeywords
from selenium import webdriver
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import timestr_to_secs
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from libs.ui.AutoException import *
from libs.ui.UIPerformanceTimer import UIPerformanceTimer
from libs.ui.DataTable import DataTable
from libs.ui.constants_browsers_drivers import BROWSERS
from libs.variables.defaults import DEFAULTS

from selenium.webdriver.support.ui import WebDriverWait

from libs.ui.AutoException import BrowserPageNotLoadedException, AutoException, AssertionErrorException

WAIT_FOR_SCRIPT = """
try { return (function (rootSelector, callback) {
  var el = document.querySelector(rootSelector);

  try {
    if (!window.angular) {
      throw new Error('angular could not be found on the window');
    }
    if (angular.getTestability) {
      angular.getTestability(el).whenStable(callback);
    } else {
      if (!angular.element(el).injector()) {
        throw new Error('root element (' + rootSelector + ') has no injector.' +
           ' this may mean it is not inside ng-app.');
      }
      angular.element(el).injector().get('$browser').
          notifyWhenNoOutstandingRequests(callback);
    }
  } catch (err) {
    callback(err.message);
  }
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }
"""

js_waiting_var = """
#     var waiting = true;
#     var callback = function () {waiting = false;}
#     var el = document.querySelector('#nested-ng-app');
#     angular.element(el).injector().get('$browser').
#                 notifyWhenNoOutstandingRequests(callback);
#     return waiting;
# """

js_wait_for_angular = """
    var waiting = true;
    var callback = function () {waiting = false;}
    var el = document.querySelector(arguments[0]);
    if (window.angular && !(window.angular.version &&
          window.angular.version.major > 1)) {
      /* ng1 */
      angular.element(el).injector().get('$browser').
          notifyWhenNoOutstandingRequests(callback);
    } else if (window.getAngularTestability) {
      return !window.getAngularTestability(el).isStable(callback);
    } else if (window.getAllAngularTestabilities) {
      throw new Error('AngularJSLibrary does not currently handle ' +
          'window.getAllAngularTestabilities. It does work on sites supporting ' +
          'window.getAngularTestability. If you require this functionality, please ' +
          'the library authors or reach out to the Robot Framework Users Group.');
    } else if (!window.angular) {
      throw new Error('window.angular is undefined.  This could be either ' +
          'because this is a non-angular page or because your test involves ' +
          'client-side navigation. Currently the AngularJS Library is not ' +
          'designed to wait in such situations. Instead you should explicitly ' +
          'call the "Wait For Angular" keyword.');
    } else if (window.angular.version >= 2) {
      throw new Error('You appear to be using angular, but window.' +
          'getAngularTestability was never set.  This may be due to bad ' +
          'obfuscation.');
    } else {
      throw new Error('Cannot get testability API for unknown angular ' +
          'version "' + window.angular.version + '"');
    }
    return waiting;
"""

js_wait_for_angularjs = """
    var callback = arguments[0];
    var el = document.querySelector('[ng-app]');
    if (typeof angular.element(el).injector() == "undefined") {
        throw new Error('root element ([ng-app]) has no injector.' +
                       ' this may mean it is not inside ng-app.');
    }
    angular.element(el).injector().get('$browser').notifyWhenNoOutstandingRequests(callback);
"""

js_repeater_min = """var rootSelector=null;function byRepeaterInner(b){var a="by."+(b?"exactR":"r")+"epeater";return function(c){return{getElements:function(d){return findAllRepeaterRows(c,b,d)},row:function(d){return{getElements:function(e){return findRepeaterRows(c,b,d,e)},column:function(e){return{getElements:function(f){return findRepeaterElement(c,b,d,e,f,rootSelector)}}}}},column:function(d){return{getElements:function(e){return findRepeaterColumn(c,b,d,e,rootSelector)},row:function(e){return{getElements:function(f){return findRepeaterElement(c,b,e,d,f,rootSelector)}}}}}}}}repeater=byRepeaterInner(false);exactRepeater=byRepeaterInner(true); function repeaterMatch(a,b,c){if(c){return a.split(" track by ")[0].split(" as ")[0].split("|")[0].split("=")[0].trim()==b}else{return a.indexOf(b)!=-1}}function findRepeaterRows(k,e,g,l){l=l||document;var d=["ng-","ng_","data-ng-","x-ng-",arguments[1]]; var o=[];for(var a=0;a<d.length;++a){var h=d[a]+"repeat";var n=l.querySelectorAll("["+h+"]");h=h.replace(arguments[0]);for(var c=0;c<n.length;++c){if(repeaterMatch(n[c].getAttribute(h),k,e)){o.push(n[c])}}}var f=[];for(var a=0;a<d.length;++a){var h=d[a]+"repeat-start";var n=l.querySelectorAll("["+h+"]");h=h.replace(arguments[0]);for(var c=0;c<n.length;++c){if(repeaterMatch(n[c].getAttribute(h),k,e)){var b=n[c];var m=[];while(b.nodeType!=8||!repeaterMatch(b.nodeValue,k)){if(b.nodeType==1){m.push(b)}b=b.nextSibling}f.push(m)}}}var m=o[g]||[],j=f[g]||[];return[].concat(m,j)}function findAllRepeaterRows(g,e,h){h=h||document;var k=[];var d=["ng-","ng_","data-ng-","x-ng-",arguments[1]];for(var a=0;a<d.length;++a){var f=d[a]+"repeat";var j=h.querySelectorAll("["+f+"]");f=f.replace(arguments[0]);for(var c=0;c<j.length;++c){if(repeaterMatch(j[c].getAttribute(f),g,e)){k.push(j[c])}}}for(var a=0;a<d.length;++a){var f=d[a]+"repeat-start";var j=h.querySelectorAll("["+f+"]");f=f.replace(arguments[0]);for(var c=0;c<j.length;++c){if(repeaterMatch(j[c].getAttribute(f),g,e)){var b=j[c];while(b.nodeType!=8||!repeaterMatch(b.nodeValue,g)){if(b.nodeType==1){k.push(b)}b=b.nextSibling}}}}return k}function findRepeaterElement(a,b,g,r,q,w){var c=[];var t=document.querySelector(w||"body");q=q||document;var l=[];var x=["ng-","ng_","data-ng-","x-ng-",arguments[1]];for(var n=0;n<x.length;++n){var s=x[n]+"repeat";var o=q.querySelectorAll("["+s+"]");s=s.replace(arguments[0]);for(var v=0;v<o.length;++v){if(repeaterMatch(o[v].getAttribute(s),a,b)){l.push(o[v])}}}var m=[];for(var n=0;n<x.length;++n){var s=x[n]+"repeat-start";var o=q.querySelectorAll("["+s+"]");s=s.replace(arguments[0]);for(var v=0;v<o.length;++v){if(repeaterMatch(o[v].getAttribute(s),a,b)){var y=o[v];var f=[];while(y.nodeType!=8||(y.nodeValue&&!repeaterMatch(y.nodeValue,a))){if(y.nodeType==1){f.push(y)}y=y.nextSibling}m.push(f)}}}var f=l[g];var z=m[g];var A=[];if(f){if(f.className.indexOf("ng-binding")!=-1){A.push(f)}var k=f.getElementsByClassName("ng-binding");for(var v=0;v<k.length;++v){A.push(k[v])}}if(z){for(var v=0;v<z.length;++v){var e=z[v];if(e.className.indexOf("ng-binding")!=-1){A.push(e)}var k=e.getElementsByClassName("ng-binding");for(var u=0;u<k.length;++u){A.push(k[u])}}}for(var v=0;v<A.length;++v){var h=angular.element(A[v]).data("$binding");if(h){var d=h.exp||h[0].exp||h;if(d.indexOf(r)!=-1){c.push(A[v])}}}return c}function findRepeaterColumn(a,b,q,o,w){var c=[];var s=document.querySelector(w||"body");o=o||document;var h=[];var x=["ng-","ng_","data-ng-","x-ng-",arguments[1]];for(var m=0;m<x.length;++m){var r=x[m]+"repeat";var n=o.querySelectorAll("["+r+"]");r=r.replace(arguments[0]);for(var v=0;v<n.length;++v){if(repeaterMatch(n[v].getAttribute(r),a,b)){h.push(n[v])}}}var l=[];for(var m=0;m<x.length;++m){var r=x[m]+"repeat-start";var n=o.querySelectorAll("["+r+"]");r=r.replace(arguments[0]);for(var v=0;v<n.length;++v){if(repeaterMatch(n[v].getAttribute(r),a,b)){var y=n[v];var e=[];while(y.nodeType!=8||(y.nodeValue&&!repeaterMatch(y.nodeValue,a))){if(y.nodeType==1){e.push(y)}y=y.nextSibling}l.push(e)}}}var z=[];for(var v=0;v<h.length;++v){if(h[v].className.indexOf("ng-binding")!=-1){z.push(h[v])}var g=h[v].getElementsByClassName("ng-binding");for(var t=0;t<g.length;++t){z.push(g[t])}}for(var v=0;v<l.length;++v){for(var u=0;u<l[v].length;++u){var y=l[v][u];if(y.className.indexOf("ng-binding")!=-1){z.push(y)}var g=y.getElementsByClassName("ng-binding");for(var t=0;t<g.length;++t){z.push(g[t])}}}for(var u=0;u<z.length;++u){var f=angular.element(z[u]).data("$binding");if(f){var d=f.exp||f[0].exp||f;if(d.indexOf(q)!=-1){c.push(z[u])}}}return c};"""


root_selector = "[ng-app]"
implicit_angular_wait = 60.0
prefixes = ['ng-click', 'ng', 'ng-model', 'ng-value', 'ng-class', 'ng-repeat', 'ng-bind']
ng_methods = ['_find_by_click', '_find_by_model', '_find_by_binding', '_find_by_ng_repeater']
arg0 = "/\\/g,\"\""
arg1 = "ng\\:"


def strip_curly_braces(binding):
    """ Starting with AngularJS 1.3 the interpolation brackets are not allowed
    in the binding description string. As such the AngularJSLibrary strips them
    out before calling the _find_by_binding method.
    See http://www.protractortest.org/#/api?view=ProtractorBy.prototype.binding
    """
    if binding.startswith('{{'):
        binding = binding[2:]
    if binding.endswith('}}'):
        binding = binding[:-2]
    return binding


class ExtendedSeleniumLibrary(SeleniumLibrary):

    """ Extended SeleniumLibrary is the web  GUI library for Robot Framework.
        This Library has been built by Extending Robot Selenium library and using Robot Angular JS libraries.
        Library contains all Robot Selenium keywords that are customised by extending relevant
        SeleniumLibrary keywords. Extended SeleniumLibrary uses the Selenium Library modules internally
        to control a web browser and perform actions.

        For more details on Selenium Library - Please visit
        "https://github.com/robotframework/SeleniumLibrary"

        To write methods/keywords in the python modules for Robot Framework, ExtendedSeleniumLibrary must be
        imported into your basepage which in turn will inherited by other GUI python modules.

    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LISTENER_API_VERSION = 2

    DO_NOT_CAPTURE_KEYWORDS = [
        "Run Keyword And Ignore Error",
        "Run Keyword And Expect Error",
        "Run Keyword And Return Status",
        "Wait Until.*"
    ]

    def __init__(self, ignore_implicit_angular_wait=False):

        super(ExtendedSeleniumLibrary, self).__init__(
            timeout=60,
            implicit_wait=60,
            run_on_failure='Capture Page Screenshot'
        )

        self.ROBOT_LIBRARY_LISTENER = self
        self._is_current_keyword_inside_teardown = False
        self._do_not_capture_parent_keywords_count = 0
        self._screenshot_was_captured = False
        self.alert = AlertKeywords(self)
        self.browser = BrowserManagementKeywords(self)
        self.cookie = CookieKeywords(self)
        self.element = ElementKeywords(self)
        self.form_element = FormElementKeywords(self)
        self.frame = FrameKeywords(self)
        self.ignore_implicit_angular_wait = ignore_implicit_angular_wait
        self.javascript = JavaScriptKeywords(self)
        self.screenshot = ScreenshotKeywords(self)
        self.select = SelectElementKeywords(self)
        self.table = TableElementKeywords(self)
        self.wait = WaitingKeywords(self)
        self.window = WindowKeywords(self)

        if not root_selector:
            self.root_selector = '[ng-app]'
        else:
            self.root_selector = root_selector

        # Override default locators to include binding {{ }}
        self.element._element_finder = NGElementFinder(
            self.root_selector,
            self.ignore_implicit_angular_wait,
            self._selenium
        )
        # Add Angular specific locator strategies
        self.element.add_location_strategy('ng-binding', self._find_by_binding, persist=True)
        self.element.add_location_strategy('binding', self._find_by_binding, persist=True)
        self.element.add_location_strategy('ng-click', self._find_by_click, persist=True)
        self.element.add_location_strategy('click', self._find_by_click, persist=True)
        self.element.add_location_strategy('ng-model', self._find_by_model, persist=True)
        self.element.add_location_strategy('model', self._find_by_model, persist=True)
        self.element.add_location_strategy('ng-repeater', self._find_by_ng_repeater, persist=True)
        self.element.add_location_strategy('repeater', self._find_by_ng_repeater, persist=True)

    @property
    def _selenium(self):
        return self

    @property
    def _selenium_driver(self):
        return self._selenium.driver

    def get_page_loading_timers(self, ajax_wait=0.0):
        """ Use Navigation Timing  API to calculate the timings that matter the most """

        # logger.debug("Reading the UI Performance and Paint Event Counters")
        timer_ui_performance = UIPerformanceTimer()
        timer_ui_performance.time_ajax_wait = ajax_wait
        ui_perf_data = self.driver.execute_script("return window.performance.timing;")
        ui_perf_data_paint = self.driver.execute_script("return window.performance.getEntriesByType('paint');")

        timer_ui_performance.navigationStart = ui_perf_data['navigationStart']
        timer_ui_performance.unloadEventStart = ui_perf_data['unloadEventStart']
        timer_ui_performance.unloadEventEnd = ui_perf_data['unloadEventEnd']
        timer_ui_performance.redirectStart = ui_perf_data['redirectStart']
        timer_ui_performance.redirectEnd = ui_perf_data['redirectEnd']
        timer_ui_performance.fetchStart = ui_perf_data['fetchStart']
        timer_ui_performance.domainLookupStart = ui_perf_data['domainLookupStart']
        timer_ui_performance.domainLookupEnd = ui_perf_data['domainLookupEnd']
        timer_ui_performance.connectStart = ui_perf_data['connectStart']
        timer_ui_performance.connectEnd = ui_perf_data['connectEnd']
        timer_ui_performance.secureConnectionStart = ui_perf_data['secureConnectionStart']
        timer_ui_performance.requestStart = ui_perf_data['requestStart']
        timer_ui_performance.responseStart = ui_perf_data['responseStart']
        timer_ui_performance.responseEnd = ui_perf_data['responseEnd']
        timer_ui_performance.domLoading = ui_perf_data['domLoading']
        timer_ui_performance.domInteractive = ui_perf_data['domInteractive']
        timer_ui_performance.domContentLoadedEventStart = ui_perf_data['domContentLoadedEventStart']
        timer_ui_performance.domContentLoadedEventEnd = ui_perf_data['domContentLoadedEventEnd']
        timer_ui_performance.domComplete = ui_perf_data['domComplete']
        timer_ui_performance.loadEventStart = ui_perf_data['loadEventStart']
        timer_ui_performance.loadEventEnd = ui_perf_data['loadEventEnd']

        # logger.debug("%s" % ("=" * 100))
        # logger.debug("Performance Counters:\n%s\n" % repr(ui_perf_data))
        # logger.debug("%s" % ("-" * 100))
        # logger.debug("Paint Event Counters:\n%s\n" % repr(ui_perf_data_paint))
        # logger.debug("%s" % ("-" * 100))
        # logger.debug("Performance Data:\n%s\n" % timer_ui_performance)
        # logger.debug("%s" % ("=" * 100))

        return timer_ui_performance

    def _find_by_binding(self, browser, criteria, tag, constrains):
        return browser.execute_script(
            """
            var binding = '%s';
            var bindings = document.getElementsByClassName('ng-binding');
            var matches = [];
            for (var i = 0; i < bindings.length; ++i) {
                var dataBinding = angular.element(bindings[i]).data('$binding');
                if(dataBinding) {
                    var bindingName = dataBinding.exp || dataBinding[0].exp || dataBinding;
                    if (bindingName.indexOf(binding) != -1) {
                        matches.push(bindings[i]);
                    }
                }
            }
            return matches;""" % criteria
        )

    def _find_by_click(self, browser, criteria, tag, constraints):

        ng_prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-']
        elements = []

        for prefix in ng_prefixes:
            selector_xpath = criteria
            locator = criteria
            if isinstance(criteria, (list, tuple)):
                by = criteria[0]
                locator = str(criteria[1])
                locator = locator.replace("'", '"').replace('"', '\"')
                selector_xpath = (by, locator)

            selector_xpath = locator.replace('"', r'\"')
            selector = "[%sclick='%s']" % (prefix, selector_xpath)
            logger.debug("_find_by_click | Selector: %s" % selector)
            script_cmd = "return document.querySelectorAll(\"%s\");" % selector
            logger.debug("_find_by_click | Script Command: %s" % script_cmd)
            elements = browser.execute_script(script_cmd)

            if elements:
                break

        if elements is None:
            elements = []

        logger.debug("_find_by_click | NG Elements count: %d" % len(elements))
        if not len(elements):
            raise ValueError("_find_by_click | No matching Elements | Locator: %s" % str(criteria))

        return ElementFinder(ctx=self._selenium)._filter_elements(elements, tag, constraints)

    def _find_by_model(self, browser, criteria, tag, constraints):

        ng_prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-']
        elements = None

        for prefix in ng_prefixes:
            selector = '[%smodel="%s"]' % (prefix, criteria)
            logger.debug("_find_by_model | Selector: %s" % repr(selector))
            elements = browser.execute_script("""return document.querySelectorAll('%s');""" % selector)

            if elements:
                break

        if elements is None:
            elements = []
        logger.debug("_find_by_model | NG Elements Count: %d" % len(elements))

        if not len(elements):
            raise ValueError("_find_by_model | No matching Elements | Locator: %s" % str(criteria))

        return ElementFinder(ctx=self._selenium)._filter_elements(elements, tag, constraints)

    def _find_ng_elements(self, element, tag=None, constraints=None):

        ng_elements = None

        for ng_method in ng_methods:
            func = self.__getattribute__(ng_method)
            logger.debug("_find_ng_elements | Method: %s" % ng_method)
            ng_elements = func(self._selenium_driver, element, tag, constraints)

            if ng_elements:
                break

        if ng_elements is None:
            ng_elements = []

        logger.debug("_find_ng_elements | NG Elements Count: %d" % len(ng_elements))
        return ng_elements

    def _find_by_ng_repeater(self, browser, criteria, tag, constraints):

        repeater_row_col = self._parse_ng_repeat_locator(criteria)
        js_repeater_str = self._reconstruct_js_locator(repeater_row_col)
        logger.debug("Variable | js_repeater_str: %s" % js_repeater_str)
        elements = browser.execute_script(
            """%s var ng_repeat = new byRepeaterInner(true);
            return ng_repeat%s.getElements();""" % (js_repeater_min, js_repeater_str),
            arg0, arg1
        )

        if not elements:
            elements = []

        logger.debug("_find_by_ng_repeater | NG Elements Count: %d" % len(elements))

        if not elements:
            raise ValueError("_find_by_ng_repeater | Element locator '%s' did not match any elements." % str(criteria))

        return ElementFinder(ctx=self._selenium)._filter_elements(elements, tag, constraints)

    def _parse_ng_repeat_locator(self, criteria):

        def _split_by_separator(str_array, sep):
            if str_array.startswith(sep):
                return str_array.split(sep, 1)[-1]
            else:
                return None

        def _parse_array_with_regex(str_array):
            import re
            match = re.search(r"(?<=^\[).+([0-9]*).+(?=\]$)", str_array)
            if match:
                return match.group()
            else:
                return None

        def _parse_array(str_array):
            if str_array[0] == '[' and str_array[-1] == ']':
                return int(str_array[1:-1])
            else:
                return None

        rrc = criteria.rsplit('@')
        extracted_element = {
            'repeater': None,
            'row_index': None,
            'col_binding': None
        }

        if len(rrc) == 1:
            # is only repeater
            extracted_element['repeater'] = rrc[0]
            return extracted_element
        else:
            # for index in reversed(rrc):
            while 1 < len(rrc):
                index = rrc.pop()
                row = _split_by_separator(index, 'row')
                column = _split_by_separator(index, 'column')

                if row:
                    array = _parse_array(row)
                    row_locator = _split_by_separator(row, '=')

                    if array is not None:
                        extracted_element['row_index'] = array
                    elif row_locator:
                        # row should be an list index and not binding locator
                        raise ValueError("AngularJS ng-repeat locator with row as binding is not supported")

                elif column:
                    array = _parse_array(column)
                    column_locator = _split_by_separator(column, '=')

                    if array is not None:
                        # col should be an binding locator and not list index
                        raise ValueError("AngularJS ng-repeat locator with column as index is not supported")
                    elif column_locator:
                        extracted_element['col_binding'] = column_locator

                rrc[-1] = '%s@%s' % (rrc[-1], index)

        extracted_element['repeater'] = rrc[0]
        return extracted_element

    def _reconstruct_js_locator(self, loc_dict):
        js_locator = "(\"%s\")" % loc_dict['repeater']

        if loc_dict['row_index']:
            js_locator = "%s.row(%s)" % (js_locator, loc_dict['row_index'])

        if loc_dict['col_binding']:
            js_locator = "%s.column(\"%s\")" % (js_locator, loc_dict['col_binding'])

        logger.debug("_reconstruct_js_locator | js_locator: %s" % js_locator)
        return js_locator

    def wait_for_angular(self, timeout=None, error=None, track_ui_loading_time=True):
        """
        An explicit wait allowing Angular queue to empty.

        With the implicit wait functionality it is expected that most of the
        situations where waiting is needed will be handled "automatically" by
        the "hidden" implicit wait. Thus it is expected that this keyword will
        be rarely used.
        """
        logger.debug("Waiting for Angular pages to load...")
        ui_timers = None

        time_wait_start = time.time()
        try:
            self.driver.set_script_timeout(timeout)
            # self.driver.execute_async_script(WAIT_FOR_SCRIPT)

            WebDriverWait(
                self._selenium_driver,
                timeout=timeout,
                poll_frequency=1,
                ignored_exceptions=(WebDriverException,)
            ).until_not(
                    lambda x: self._selenium_driver.execute_script(
                        js_wait_for_angular, root_selector
                    )
            )
        except Exception as excp:
            logger.debug("HANDLED_EXCEPTION | Details: %s" % repr(excp))

        time_wait_end = time.time()
        time_angular_wait = (time_wait_end - time_wait_start) * 1000
        logger.debug("wait_for_angular | Waited for: %f" % round(time_angular_wait, 2))

        if track_ui_loading_time:
            ui_timers = self.get_page_loading_timers(ajax_wait=time_angular_wait)

        return ui_timers

    def wait_for_element_to_load(self, element, timeout=None):
        """ Method to element to load based on Angular and Non Angular wait time.
            Method will wait for both angular and non angular element based on the element passed automatically.
            No seperate mechanism needed in pages or tests to denote angular or non angular waits
                   :Parameters:
                       - element : element to be loaded, not a locator
                       - timeout : timeout to wait for element to load
                   Default browser opened is Firefox
                   Examples:
                       | wait_for_element_to_load |element=(By.ID,"user_email"),timeout=60
        """

        element_attrs = self.driver.execute_script(
            """
            var items = {}; 
            for (index=0; index<arguments[0].attributes.length; ++index) { 
                items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value
            };
            return items;
            """,
            element
        )
        attrs_value = [key for key, value in element_attrs.items() if 'ng' in key.lower()]
        # logger.info('Attributes Value: %s' % attrs_value)

        if any(i in prefixes for i in attrs_value):
            self.wait_for_angular(timeout=implicit_angular_wait)
        else:
            logger.debug("Starting Non-Angular wait...")
            self.wait.wait_until_page_contains_element(element)
        return

    @keyword(name="Get Current Browser Desired Capabilities")
    def get_current_browser_desired_capabilities(self):
        logger.info('Getting currently open browser desired capabilities')
        return self.driver.desired_capabilities

    @keyword(name="Switch To Browser Window With Title")
    def switch_to_browser_window_with_title(self, locator='NEW'):
        """Method to get windows titles and switch to next new window"""
        logger.debug("Getting windows titles...")
        titles = self.window.get_window_titles
        logger.debug("Windows Titles: %s" % repr(titles))
        if locator in titles:
            logger.debug("Locator found in Window Titles. Switching window | Locator: %s" % repr(locator))
            self.window.select_window(locator)
        else:
            logger.debug("Locator NOT found in Window Titles. Switching window (BLIND) | Locator: %s" % repr(locator))
            self.window.select_window(locator)

    @keyword
    def open_browser(self, dut_url=None, web_browser=BROWSERS.CHROME):
        """ Method to Open Browser
                :Parameters:
                    - dut_url: "application url"
                    -web_browser:  firefox,chrome,ie,phantomjs,etc.,
                Default browser opened is Firefox
                Examples:
                    | open_browser | dut_url=portal.stgcom,web_browser=chrome
                """

        try:
            url = dut_url
            if url and not url.startswith('http'):
                url = 'https://%s' % url

            logger.info("Open browser: %s | URL: %s" % (web_browser, url))

            if web_browser == BROWSERS.CHROME:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("no-sandbox")
                chrome_options.add_argument('--ignore-certificate-errors')
                # chrome_options.add_argument('--incognito')
                self.browser.open_browser(browser=web_browser, options=chrome_options)
            else:
                self.browser.open_browser(browser=web_browser)

            if url:
                self.browser.go_to(url)

            self.driver.set_page_load_timeout(60)
            logger.debug('Successfully launched the Browser.')

        except Exception as e:
            logger.debug('EXCEPTION | open_browser | Details: %s' % repr(e))
            raise BrowserPageNotLoadedException(e)

    @keyword
    def close_browser(self):
        """
        Method to Close Browser
            :Parameters:
                - None
            Default browser opened is Firefox
            Examples:
                | close_browser |
        """
        self.browser.close_browser()
        logger.debug('Browser closed successfully')

    @keyword
    def maximize_window(self):
        """
        Method to maximise Browser
            :Parameters:
                - None
            Default browser opened is Firefox
            Examples:
                | maximize_window |
        """
        self.driver.maximize_window()
        logger.debug('Browser window maximised')

    @keyword(name="Navigate To")
    def navigate_to(self, url):
        """ Method to Open Browser
                :Parameters:
                    - dut_url: "application url"
                    -web_browser:  firefox,chrome,ie,phantomjs,etc.,
                Default browser opened is Firefox
                Examples:
                    | open_browser | dut_url=portal.stgcom,web_browser=chrome
                """

        if not url:
            logger.error("No URL Provided.")
        else:
            try:
                if not url.startswith('http'):
                    url = 'https://%s' % url

                self.driver.set_page_load_timeout(60)
                self.browser.go_to(url)

                logger.debug('Successfully launched the URL in Browser.')

            except Exception as e:
                logger.debug('EXCEPTION | navigate_to | Details: %s' % repr(e))
                raise BrowserPageNotLoadedException(e)

    @keyword(name="Is Element Present")
    def is_element_present(self, element, timeout=implicit_angular_wait):
        """ Method to check if element is present"""
        try:
            presence_element = self.driver.find_element(*element)
            self.wait_for_element_to_load(presence_element, timeout)
            presence_element.is_displayed()
            logger.info("Element is present | Element: %s" % repr(element))
            return True
        except:
            return False

    @keyword(name="Is Text Present")
    def is_text_present(self, text):
        """ Method to check if text is present
                                         """
        try:
            self.wait.wait_until_page_contains(text)
            text_present = self.element.page_should_contain(text)
            logger.info("Text is present in the page | Text: %s" % text_present)
            return True
        except:
            return False

    @keyword(name="Clear")
    def clear(self, element, value=None, tag=None, constraints=None):
        """
        Method to clear text element. Bundles both ng and normal elements automatically.

        Parameters:
            element : "element to be clicked"
            value: "Value associated with element if any
            tag : Element tag"
            constraints: constraints

        E.g:
            self.send_keys(element=(By.ID,"password"),text_value="abc@gmail.com",value="User Password")
            self.send_keys(element="//$ctrl.data=ctrl-l1pclk", text_value="abc@gmail.com", value="User Name")
        """
        if constraints is None:
            constraints = {}

        if isinstance(element, tuple):
            try:
                text_element = self.driver.find_element(*element)
                self.wait_for_element_to_load(text_element, 20)
                self.element.clear_element_text(text_element)
                logger.info("Text Cleared | Field: %s" % repr(element))
            except NoSuchElementException as e:
                raise NoSuchElementException(element, e)

        elif isinstance(element, str):
            elements = self._find_ng_elements(element, tag, constraints)

            for text_element in elements:
                if value in text_element.text:
                    try:
                        text_element.clear()
                        logger.info("Text Cleared | Field: %s" % text_element)
                    except:
                        pass
                    return

            raise ValueError("Element NOT Found | Element: %s" % str(element))

    @keyword(name="Click")
    def click(self, element, value=None, tag=None, constraints=None):
        """
        Method to click an element. Handles both ng and normal elements automatically.
        Parameters:
              element: "element to be clicked"
              value: "Value associated with element if any"
              tag: "Element tag"
              constraints: constraints

        E.g:
        self.click(element=(By.ID,"username"), value="User Name")
        self.click(element="//$ctrl.data=ctrl-l1ngclick", value="User Name")
        """
        if constraints is None:
            constraints = {}

        if isinstance(element, (tuple, list)):
            try:
                clickable_element = self.driver.find_element(*element)
                logger.debug("ESL::click() | NOT_NG: Clickable Element: %s" % repr(clickable_element))
                self.wait_for_element_to_load(clickable_element)
                time.sleep(1)
                clickable_element.click()
                logger.info("ESL::click() | NOT_NG: Clicked element | Identifier: %s" % repr(element))

            except ElementClickInterceptedException as e:
                logger.debug("ESL::click() | EXCEPTION | Details: %s" % repr(e))
                raise ElementClickInterceptedException(element, e)
            except NoSuchElementException as e:
                logger.debug("ESL::click() | EXCEPTION | Details: %s" % repr(e))
                raise NoSuchElementException(element, e)

        elif isinstance(element, str):
            elements = self._find_ng_elements(element, tag, constraints)

            if not elements:
                raise ValueError("Element locator did not match any elements | Locator: %s" % str(element))

            for clickable_element in elements:
                self.wait_for_element_to_load(clickable_element, timeout=1)
                logger.debug("ESL::click() | Current Text: %s | Input Text: %s" % (clickable_element.text, value))

                clk_text = clickable_element.text
                logger.debug("ESL::click() | NG: Clickable Element Text: %s" % clk_text)
                if value and value in clk_text:    # clickable_element.text:
                    logger.info("ESL::click() | NG.Click | Value: %s | Clickable Text: %s" % (value, clk_text))
                    clickable_element.click()
                    return

                if not value:
                    logger.info("ESL::click() | NG.Click | Empty Value | Clickable Text: %s" % (clk_text))
                    time.sleep(1)
                    clickable_element.click()
                    return

            raise ValueError("Could not CLICK Element locator | Locator: %s" % str(element))

    @keyword(name="Double Click")
    def double_click(self, element):
        """ Method to double click item from list"""
        try:
            doubleclick_element = self.driver.find_element(*element)
            self.wait_for_element_to_load(doubleclick_element)
            self.action.double_click(doubleclick_element).perform()
            logger.info("Double clicked element | Element: %s" % repr(element))
        except NoSuchElementException as e:
            raise NoSuchElementException(element, e)

    @keyword(name="Find Element Ex")
    def find_element_extended(self, element, value=None, tag=None, constraints=None):
        """ Method to find an element. Handles both ng and normal elements automatically.
                Parameters:
                      element: "element to be clicked"
                      value: "Value associated with element if any"
                      tag: "Element tag"
                      constraints: constraints

                E.g:
                self.find_element_extended(element=(By.ID,"username"), value="User Name")
                self.find_element_extended(element="//$ctrl.data=ctrl-l1ngclick", value="User Name")
        """
        if constraints is None:
            constraints = {}

            found_element = None
            self.driver.implicitly_wait(5)
            if isinstance(element, (list, tuple)):
                try:
                    logger.debug("find_element_extended | NOT_NG: Element (Is Tuple): %s" % repr(element))
                    found_element = self.driver.find_element(*element)
                    logger.debug("find_element_extended | NOT_NG: Clickable Element: %s" % repr(found_element))
                    self.wait_for_element_to_load(found_element)
                    logger.info("find_element_extended | FOUND_ELEMENT-NOT_NG: Element: %s" % str(element))

                except Exception as e:
                    logger.debug("find_element_extended | EXCEPTION | Details: %s" % repr(e))
                    logger.debug("find_element_extended | Trying NG")
                    elements = self._find_ng_elements(element, tag, constraints)

                    if not elements:
                        raise ValueError("Element locator did not match any elements | Locator: %s" % str(element))

                    for element in elements:
                        self.wait_for_element_to_load(element, timeout=1)

                        if not value:
                            found_element = element
                            break

                        clk_text = element.text
                        logger.debug("find_element_extended | Current Text: %s" % clk_text)

                        if value == clk_text:  # found_element.text:
                            found_element = element
                            logger.info(
                                "find_element_extended | FOUND_ELEMENT-NG | Element: %s | Clickable Text: %s" % (repr(found_element), clk_text))
                            break

            else:
                found_element = self.driver.find_element(element)

            self.driver.implicitly_wait(10)
            return found_element

    @keyword
    def get_text(self, element, timeout=None):
        """ Method to get a text from a specific element """

        try:
            text_element = self.driver.find_element(*element)
            self.wait_for_element_to_load(text_element, timeout)
            text = self.element.get_text(text_element)
            logger.info("Get Text | Element: %s | Text: %s" % (str(text_element), text))
            return text
        except Exception as e:
            logger.error("EXCEPTION | %s" % repr(e))
            raise AutoException(e)

    @keyword
    def get_value(self, element):
        try:
            value_element = self.driver.find_element(*element)
            self.wait_for_element_to_load(value_element)
            value = self.element.get_value(value_element)
            logger.info("Text from element | Element: %s | Value: %s" % (value_element, value))
            return value
        except AutoException as e:
            raise AutoException(e)

    @keyword
    def input_text(self, element, text_value, value=None, tag=None, constraints=None):
        """
        Method to input text into an element. Bundles both ng and normal elements automatically.

        Parameters:
            element : "element to be clicked"
            text_value : "value to be input in text field
            value: "Value associated with element if any
            tag : Element tag"
            constraints: constraints

        E.g:
            self.input_text(element=(By.ID,"password"),text_value="abc@gmail.com",value="User Password")
            self.input_text(element="//$ctrl.data=ctrl-l1pclk", text_value="abc@gmail.com", value="User Name")
        """
        self.send_keys(element, text_value, value, tag, constraints)

    @keyword(name="Input Text In Popup Window")
    def input_text_in_popup_window(self, text):
        """ Method to input text in any pop up alert"""
        try:
            if self.alert.alert_should_be_present:
                self.alert.input_text_into_alert(text)
            logger.info("Text entered into popup window | Text: %s" % text)
        except AutoException as e:
            raise AutoException(e)

    # @keyword(name="Mouse Over")
    # def mouse_over(self, element):
    #
    #     if isinstance(element, (tuple, list)):
    #         element = element[1]
    #
    #     # element_to_hover_over = self.driver.find_element(element)
    #     # hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
    #     # hover.perform()
    #     self._selenium.mouse_over(element)
    #     return

    @keyword(name="NG Select From List")
    def ng_select_from_list(self, criteria, value=None, tag=None, constraints=None):
        """Method to select from ng list"""

        if constraints is None:
            constraints = {}
        clickable_element = None

        try:
            elements = self._find_by_click(self.driver, criteria, tag, constraints)
            for clickable_element in elements:
                if value in clickable_element.text:
                    clickable_element.click()
                    return

            raise ValueError("Element locator '%s' did not match any elements." % criteria)

        except NoSuchElementException as e:
            raise NoSuchElementException(clickable_element, e)

    @keyword(name="Select From List")
    def select_from_list(self, option, element):
        """ Method to select item from list """

        try:
            select_element = self.driver.find_element(*element)
            self.wait_for_element_to_load(select_element)
            if option not in self.select.get_selected_list_values(select_element):
                select_element.click()
                self.select.select_from_list_by_value(select_element, option)
                logger.info("Option selected | Element: %s | Option: %s" % (element, option))
            else:
                logger.info("Option ALREADY selected | Element: %s | Option: %s" % (element, option))
        except NoSuchElementException as e:
            raise NoSuchElementException(element, e)

    @keyword(name="js_checkbox_operation_by_name")
    def js_checkbox_operation_by_name(self, element_name, select=True):
        """
        js_checkbox_operation_by_name
            - Find an element by javascript search on the DOM document

            :Parameters:
            :param element:
                -   Element to find as 'element_type=name'
        """

        cb_selection_code = """ if(cb_element.checked == true){ cb_element.click(); } """
        if select:
            cb_selection_code = """ if(cb_element.checked == false){ cb_element.click(); } """

        script_cmd = """var cb_element = 0; var cb_elements = document.getElementsByName('%s'); if (cb_elements && cb_elements.length > 0) { cb_element = cb_elements[0]; }  %s return cb_element;""" % (
            element_name,
            cb_selection_code
        )
        logger.debug("js_checkbox_operation_by_name | Element: %s | Script: %s" % (element_name, script_cmd))
        return self.driver.execute_script(script_cmd)

    @keyword(name="js_checkbox_operation_by_id")
    def js_checkbox_operation_by_id(self, element_name, select=True):
        """
        js_checkbox_operation_by_id
            - Find an element by javascript search on the DOM document

            :Parameters:
            :param element:
                -   Element to find as 'element_type=name'
        """
        cb_selection_code = """ if(cb_element.checked == true){ cb_element.click(); } """
        if select:
            cb_selection_code = """ if(cb_element.checked == false){ cb_element.click(); } """

        script_cmd = """var cb_element = 0; var cb_element = document.getElementById('%s');  %s return cb_element;""" % (
            element_name,
            cb_selection_code
        )
        logger.debug("js_checkbox_operation_by_id | Element: %s | Script: %s" % (element_name, script_cmd))
        return self.driver.execute_script(script_cmd)

    @keyword
    def select_checkbox_ex(self, element):
        self._select_unselect_checkbox_ex(element, True)

    @keyword
    def unselect_checkbox_ex(self, element):
        self._select_unselect_checkbox_ex(element, False)

    def _select_unselect_checkbox_ex(self, element, select=True):
        try:
            if isinstance(element, (list, tuple)):
                element =element[1]

            if str(element).startswith("id="):
                logger.debug("ESL::_select_unselect_checkbox_ex() | Checkbox - With ID")
                element = str(element).replace("id=", "", 1)
                select_element = self.js_checkbox_operation_by_id(element_name=element, select=select)
            elif str(element).startswith("name="):
                logger.debug("ESL::_select_unselect_checkbox_ex() | Checkbox - With Name")
                element = str(element).replace("name=", "", 1)
                select_element = self.js_checkbox_operation_by_name(element_name=element, select=select)
            else:
                logger.debug("ESL::_select_unselect_checkbox_ex() | Checkbox - With XPATH")
                dom_element = self._selenium.find_element(element)
                try:
                    dom_id = dom_element.get_property('id')
                    if not dom_id:
                        raise Exception("Element does not have ID. Element: %s" % element)
                    self.js_checkbox_operation_by_id(element_name=dom_id, select=select)

                except Exception as excp:
                    logger.debug("ESL::_select_unselect_checkbox_ex() | XPATH - Id | EXCEPTION: %s" % repr(excp))
                    try:
                        dom_name = dom_element.get_property('name')
                        if not dom_name:
                            raise Exception("Element does not have Name. Element: %s" % element)
                        select_element = self.js_checkbox_operation_by_name(element_name=dom_name, select=select)

                    except Exception as excp:
                        logger.debug("ESL::_select_unselect_checkbox_ex() | XPATH - Name | EXCEPTION: %s" % repr(excp))
                        logger.debug(
                            "ESL::_select_unselect_checkbox_ex() | EXCEPTION: %s\n"
                            "Everything failed. So one last try with click." % repr(excp)
                        )
                        self.click(element)

            time.sleep(0.5)
            return

        except NoSuchElementException as e:
            logger.debug("EXCEPTION | ESL::_select_unselect_checkbox_ex() | Element: %s" % repr(element))
            logger.debug("Details | %s" % repr(e))
            raise NoSuchElementException(repr(element), e)

    @keyword(name="Send Keys")
    def send_keys(self, element, text_value, value=None, tag=None, constraints=None):
        """
        Method to input text into an element. Bundles both ng and normal elements automatically.

        Parameters:
            element : "element to be clicked"
            text_value : "value to be input in text field
            value: "Value associated with element if any
            tag : Element tag"
            constraints: constraints

        E.g:
            self.send_keys(element=(By.ID,"password"),text_value="abc@gmail.com",value="User Password")
            self.send_keys(element="//$ctrl.data=ctrl-l1pclk", text_value="abc@gmail.com", value="User Name")
        """
        if constraints is None:
            constraints = {}

        time.sleep(0.5)
        if isinstance(element, tuple):
            try:
                text_element = self.driver.find_element(*element)
                self.wait_for_element_to_load(text_element, 5)
                self.element.clear_element_text(text_element)
                text_element.send_keys(text_value)
                logger.info("Text entered | Field: %s | Text: %s" % (repr(element), text_value))

            except NoSuchElementException as e:
                raise NoSuchElementException(repr(element), e)

        elif isinstance(element, str):
            elements = self._find_ng_elements(element, tag, constraints)

            for text_element in elements:
                if value in text_element.text:
                    text_element.send_keys(text_value)
                    return

            raise ValueError("Element NOT Found | Element: %s" % str(element))

    @keyword
    def element_should_contain(self, element, expected_text, value=None, tag=None, constraints=None):
        """Methods to check if an element contains expected text. Handles both ng and non angular identifiers"""

        if constraints is None:
            constraints = {}

        if isinstance(element, tuple):
            try:
                text_element = self.driver.find_element(*element)
                self.wait_for_element_to_load(text_element)
                self.element.element_should_contain(text_element, expected_text)
                logger.info("Element contains expected text | Expected Text: %s" % expected_text)
            except AssertionError as e:
                raise AssertionErrorException(expected_text, e)

        elif isinstance(element, str):
            elements = self._find_ng_elements(element, tag, constraints)

            for text_element in elements:
                if self.element.get_text(text_element) == expected_text:
                    return True

    @keyword
    def table_should_contain(self, text, element):
        """ Method to check if table contains a specific item
            Parameters:
                  text : "text to be searched"
                  element: "table identifier element"
        """
        try:
            table_element = self.driver.find_element(*element)
            self.wait_for_element_to_load(table_element)
            self.table.table_should_contain(table_element, text)
            logger.info("Table contains text | Text: %s" % text)
            return True
        except:
            return False

    @keyword(name="Read Table Column")
    def read_table_column(self, column_element):
        """
        Keyword to read a table column values
        """

        column_values_list = []
        try:
            try:
                column_text = self.get_text(column_element, timeout=5)
            except NoSuchElementException as e:
                raise

            logger.debug("read_table_column | Table Column Text: %s" % repr(column_text))

            if column_text:
                column_text = column_text.replace("\n", " ").replace("  ", " ").strip()

            column_values_list = column_text.split(" ")
            logger.info("Read Table Column | Values: %s" % column_values_list)
        except NoSuchElementException as e:
            raise

        return column_values_list

    @keyword(name="Read Table Columns")
    def read_table_columns(self, table_element):
        """
        Keyword to read a table columns values
        """

        column_values_list = []
        name_values_cols = [1, 3]

        try:
            for index in name_values_cols:
                element = table_element

                if isinstance(element, tuple):
                    element = element[1]
                    table_column = "%s/div[%d]" % (element, index)
                    element = (table_element[0], table_column,)
                else:
                    table_column = "%s/div[%d]" % (element, index)
                    element = table_column

                logger.debug("read_table_columns | Table Column: %s" % repr(element))
                table_column_values = self.read_table_column(element)
                logger.debug("read_table_columns | Table Column Values: %s" % repr(table_column_values))
                column_values_list.append(table_column_values)

        except NoSuchElementException as e:
            raise

        logger.info("Read Table Columns | Values: %s" % repr(column_values_list))
        table_values_list = []

        if column_values_list:
            table_values_list = list(zip(column_values_list[0], column_values_list[1]))

        return table_values_list

    @keyword(name="Read Data Table")
    def read_data_table(self, table_body, table_header=None, is_relative=False):

        data_table = DataTable()
        table_data = []
        table_header_fields = []

        try:
            if table_header:
                table_header_row = self.find_elements(table_header)
                logger.debug('read_data_table | table_header_row: %s' % repr(table_header_row))

                if table_header_row and len(table_header_row):
                    table_header_row_text = table_header_row[0].text
                    logger.debug('read_data_table | table_header_row_text: %s' % repr(table_header_row_text))

                    if table_header_row_text:
                        table_header_fields = [str(field).strip() for field in table_header_row_text.split('\n')]
                        data_table.headers = table_header_fields
                        logger.debug('read_data_table | table_header_fields: %s' % repr(table_header_fields))

        except Exception:
            raise AutoException()

        try:
            table_rows = None
            if is_relative:
                table_rows = self.find_elements(locator=table_body, parent=table_header)
            else:
                table_rows = self.find_elements(table_body)

            logger.debug('read_data_table | table_rows: %s' % repr(table_rows))

            if table_rows:
                for row in table_rows:
                    table_row_text = row.text
                    records = []
                    logger.debug('read_data_table | table_row_text: %s' % repr(table_row_text))

                    if table_row_text:
                        fields = [str(field).strip() for field in table_row_text.split('\n')]
                        logger.debug('read_data_table | fields: %s' % repr(fields))
                        data_table.add_row(fields)

                    #     if table_header_fields:
                    #         records = list(zip(table_header_fields, fields))
                    #     else:
                    #         empty_fields = ['no_name' for index in range(len(fields))]
                    #         records = list(zip(empty_fields, fields))
                    #
                    #     logger.info('read_data_table | records: %s' % repr(records))
                    #
                    # table_data.append(records)

        except Exception:
            raise AutoException()

        return data_table

    @keyword(name="Read Legends Table")
    def read_legends_table(self, table_body, table_header=None, is_relative=False, split_space=False):

        data_table = DataTable()
        table_header_row = None
        # We want faster timeout on Table reads
        self._selenium_driver.set_page_load_timeout(5)

        try:
            self.timeout = 5
            if table_header:
                table_header_row = self.find_elements(table_header)

                if table_header_row:
                    logger.debug('read_legends_table | table_header_row: %s' % repr(table_header_row))
                else:
                    logger.debug('read_legends_table | table_header_row: NOT AVAILABLE')

                if table_header_row and len(table_header_row):
                    table_header_row = table_header_row[0]
                    table_header_row_text = table_header_row.text

                    if table_header_row_text:
                        logger.debug('read_legends_table | table_header_row_text: %s' % repr(table_header_row_text))
                        table_header_fields = [str(field).strip() for field in table_header_row_text.split('\n')]
                        data_table.headers = table_header_fields
                        logger.debug('read_legends_table | table_header_fields: %s' % repr(table_header_fields))
                    else:
                        logger.debug('read_legends_table | table_header_row_text: NOT AVAILABLE')

        except Exception as excp:
            logger.debug("EXCEPTION (HANDLED) | read_legends_table | Details: %s" % repr(excp))
            raise AutoException(excp)

        finally:
            self.timeout = DEFAULTS.PAGE_LOAD_TIMEOUT

        try:
            table_rows = None
            if is_relative:
                table_rows = self.find_elements(locator=table_body, parent=table_header_row)
            else:
                table_rows = self.find_elements(table_body)

            if table_rows:
                logger.debug('read_legends_table | table_rows count: %d' % len(table_rows))

                for row in table_rows:
                    table_row_text = row.text

                    if table_row_text:
                        logger.debug('read_legends_table | table_row_text: %s' % repr(table_row_text))
                        fields = [str(field).strip() for field in table_row_text.split('\n')]

                        if split_space:
                            rest_of_fields = fields[1:]
                            fields = [fields[0], ]

                            rest_of_fields_split = []
                            for new_fields in rest_of_fields:
                                if new_fields:
                                    other_fields = (new_fields.replace("  ", "")).split(" ")
                                    rest_of_fields_split.extend(other_fields)

                            fields.extend(rest_of_fields_split)

                        logger.debug('read_legends_table | fields: %s' % repr(fields))
                        data_table.add_row(fields)
                    else:
                        logger.debug('read_legends_table | table_row_text: NOT AVAILABLE')

            else:
                logger.debug('read_legends_table | table_rows: NOT AVAILABLE')

        except Exception as excp:
            logger.debug("EXCEPTION | read_legends_table | Details: %s" % repr(excp))
            raise AutoException(excp)

        finally:
            self.timeout = DEFAULTS.PAGE_LOAD_TIMEOUT

        if not data_table.headers:
            if data_table.row_count:
                headers = [str(x) for x in range(1, len(data_table.row(1)) + 1)]
                data_table.headers = headers

        self._selenium_driver.set_page_load_timeout(60)
        return data_table

    @keyword(name="Read Graph Legends Table")
    def read_graph_legends_table(self, table_body, table_header='Messages|Percentage|Count'):

        data_table = DataTable()
        table_header_row = None

        try:
            if not table_header:
                table_header = 'no_header_1|no_header_2|no_header_3'

            logger.info('read_graph_legends_table | table_header: %s' % repr(table_header))

            if table_header and isinstance(table_header, str):
                table_header_fields = [str(field).strip() for field in table_header.split('|')]
                data_table.headers = table_header_fields
                logger.debug('read_graph_legends_table | table_header_fields: %s' % repr(table_header_fields))

        except Exception:
            raise AutoException()

        try:
            table_rows = None
            table_rows = self.find_elements(table_body)
            logger.debug('read_graph_legends_table | table_rows: %s' % repr(table_rows))

            if table_rows:
                for row in table_rows:
                    table_row_text = row.text
                    logger.debug('read_graph_legends_table | table_row_text: %s' % repr(table_row_text))

                    if table_row_text:
                        table_row_text = (table_row_text.replace('\n', ' ')).strip()
                        fields = [str(field).strip() for field in table_row_text.rsplit(' ', 2)]
                        logger.debug('read_graph_legends_table | fields: %s' % repr(fields))
                        data_table.add_row(fields)

        except Exception:
            raise AutoException()

        return data_table

    @keyword(name="Read Ribbons Container")
    def read_ribbons_container(self, ribbon_name):
        ribbon_dict = {}

        try:
            if ribbon_name:
                ribbon_elements = self.find_elements(ribbon_name)

                if ribbon_elements is None:
                    ribbon_elements = []

                ribbon_index = len(ribbon_elements)
                logger.debug("Ribbon Elements Count: %d" % len(ribbon_elements))

                for index in range(1, ribbon_index):
                    ribbon_content_list = ribbon_elements[index].text.splitlines()
                    feature_count, feature_column = ribbon_content_list
                    logger.debug('%s = %s' % (feature_column, feature_count))
                    ribbon_dict.update({feature_column: feature_count})

            logger.debug("Ribbon Data Dictionary: %s" % ribbon_dict)

        except Exception as e:
            logger.debug("EXCEPTION | read_ribbons_container | Details: %s" % repr(e))
            raise AutoException(e)

        return ribbon_dict

    @keyword(name="Read TG Metrics Table")
    def read_tg_metrics_table(self, table_xpath):

        tg_metrics_data_table = DataTable()
        tables = self.find_elements(table_xpath)

        if tables:
            for table in tables:
                table_rows = table.find_elements_by_tag_name("tr")
                table_record = []

                if table_rows:
                    for row in table_rows:
                        row_text = row.text
                        row_text = row_text.strip()
                        table_record.append(str(row_text).strip())

                    tg_metrics_data_table.add_row(table_record)

                else:
                    logger.debug("No Rows Found for Table | Table Element: %s" % repr(table))
        else:
            logger.debug("No Tables Found | XPath: %s" % table_xpath)

        return tg_metrics_data_table


class NGElementFinder(ElementFinder):
    """
    Ngelement_finder is to override the Selenium element finder so that ng elements can be identified by Selenium.
    For more details,visit -https://pypi.org/project/robotframework-angularjs/
    """

    def __init__(self, root_selector, ignore_implicit_angular_wait=False, selenium=None):

        super(NGElementFinder, self).__init__(ctx=selenium)
        self.root_selector = root_selector
        self.ignore_implicit_angular_wait = ignore_implicit_angular_wait

    def _find_by_default(self, criteria, tag, constraints, parent=None):

        if criteria.startswith('/'):
            _selenium = BuiltIn().get_library_instance('SeleniumLibrary')
            return _selenium._element_finder._find_by_xpath(criteria, tag, constraints, parent)

        elif criteria.startswith('{{'):
            criteria = strip_curly_braces(criteria)
            return self._find_by_binding(criteria, tag, constraints, parent)

        return self.find(criteria, tag, constraints, parent)

    def _find_by_binding(self, criteria, tag=None, constraints=None, parent=None):

        _selenium = BuiltIn().get_library_instance('SeleniumLibrary')
        browser = _selenium._current_browser

        return browser.execute_script("""
            var binding = '%s';
            var bindings = document.getElementsByClassName('ng-binding');
            var matches = [];
            for (var i = 0; i < bindings.length; ++i) {
                var dataBinding = angular.element(bindings[i]).data('$binding');
                if(dataBinding) {
                    var bindingName = dataBinding.exp || dataBinding[0].exp || dataBinding;
                    if (bindingName.indexOf(binding) != -1) {
                        matches.push(bindings[i]);
                    }
                }
            }
            return matches;
        """ % criteria)

    def find(self,  locator, tag=None, first_only=True, required=True, parent=None):
        _selenium = BuiltIn().get_library_instance('SeleniumLibrary')
        timeout = _selenium.get_selenium_timeout()
        timeout = timestr_to_secs(timeout)

        if not self.ignore_implicit_angular_wait:
            try:
                WebDriverWait(_selenium._current_browser(), timeout, 0.2).until_not(
                        lambda x: _selenium._current_browser().execute_script(
                            js_wait_for_angular,
                            self.root_selector
                        )
                )
            except TimeoutException:
                pass
        strategy = ElementFinder.find(self, locator=locator, tag=tag)
        return strategy


def test_ext_selenium_lib():

    sel_ex = ExtendedSeleniumLibrary()
    sel_ex.open_browser('https://google.com', 'chrome')


if __name__ == '__main__':
    test_ext_selenium_lib()
