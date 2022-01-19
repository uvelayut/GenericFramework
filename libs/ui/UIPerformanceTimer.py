import time
from robot.api import logger
from collections import OrderedDict


class UIPerformanceTimer:
    """
    UIPerformanceTimer

    Purpose:
    Track the UI Performance from multiple internal performance counters.
    """
    def __init__(self):
        self.ajax_wait = 0.0
        self.navigationStart = 0.0
        self.unloadEventStart = 0.0
        self.unloadEventEnd = 0.0
        self.redirectStart = 0.0
        self.redirectEnd = 0.0
        self.fetchStart = 0.0
        self.domainLookupStart = 0.0
        self.domainLookupEnd = 0.0
        self.connectStart = 0.0
        self.connectEnd = 0.0
        self.secureConnectionStart = 0.0
        self.requestStart = 0.0
        self.responseStart = 0.0
        self.responseEnd = 0.0
        self.domLoading = 0.0
        self.domInteractive = 0.0
        self.domContentLoadedEventStart = 0.0
        self.domContentLoadedEventEnd = 0.0
        self.domComplete = 0.0
        self.loadEventStart = 0.0
        self.loadEventEnd = 0.0

    def __str__(self):

        timer_dict = OrderedDict(
            {
                'time_end_user_experience': self.time_end_user_experience,
                'time_ajax_wait': self.time_ajax_wait,
                'time_unloadEvent': self.time_unloadEvent,
                'time_redirect': self.time_redirect,
                'time_domainLookup': self.time_domainLookup,
                'time_connect': self.time_connect,
                'time_request_roundtrip': self.time_request_roundtrip,
                'time_response': self.time_response,
                'time_domLoading': self.time_domLoading,
                'time_domContentLoadedEvent': self.time_domContentLoadedEvent,
                'time_loadEvent': self.time_loadEvent,
            }
        )
        properties_time = ["%s: %f" % (key, value) for key, value in timer_dict.items()]
        return " | ".join(properties_time)

    def __repr__(self):
        return self.__str__()

    @property
    def time_ajax_wait(self):
        return self.ajax_wait

    @time_ajax_wait.setter
    def time_ajax_wait(self,wait_time):
        self.ajax_wait = wait_time

    @property
    def time_end_user_experience(self):
        return (self.loadEventEnd - self.navigationStart) + self.ajax_wait

    @property
    def time_unloadEvent(self):
        return self.unloadEventEnd - self.unloadEventStart

    @property
    def time_redirect(self):
        return self.redirectEnd - self.redirectStart

    @property
    def time_domainLookup(self):
        return self.domainLookupEnd - self.domainLookupStart

    @property
    def time_connect(self):
        return self.connectEnd - self.connectStart

    @property
    def time_request_roundtrip(self):
        return self.responseEnd - self.requestStart

    @property
    def time_response(self):
        return self.responseEnd - self.responseStart

    @property
    def time_domLoading(self):
        return self.domComplete - self.domLoading

    @property
    def time_domContentLoadedEvent(self):
        return self.domContentLoadedEventEnd - self.domContentLoadedEventStart

    @property
    def time_loadEvent(self):
        return self.loadEventEnd - self.loadEventStart
