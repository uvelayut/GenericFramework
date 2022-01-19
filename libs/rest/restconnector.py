"""
Rest Connector
"""
import logging
import json
import requests

from datetime import datetime
from base64 import b64encode
from libs.variables.VariablesDictionary import VariablesDictionary

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def create_url(basepath, version, endpoint):
    """ Create URL """
    return "{}/v{}.0/{}".format(basepath, version, endpoint)


class RestConnector:
    """
    Rest Connector
    """

    def __init__(self):
        """
        Initialization of values
        """
        var = VariablesDictionary()
        self.param = {}
        self.body = {}
        self.files = {}
        self.header = {'Content-Type': "application/json"}
        self.request_type = "raw"
        self.proxy = {}
        self.basic_auth = ""
        self.add_basic_auth(var.get_global_variable("username", ""),
                            var.get_global_variable("password", ""))

    def add_basic_auth(self, username, password):
        """
        Adding basic Authorization
        """
        self.basic_auth = "Basic {}". \
            format(b64encode("{}:{}".format(username,
                                            password).encode()).decode('utf-8'))

    def delete_basic_auth(self):
        """
        Deleting Authorization
        """
        self.basic_auth = ""

    # Param Operations
    def add_param(self, data):
        """ Adding of parameters """
        self.param = data

    def append_param(self, data):
        """ Appending Parameters """
        self.param.update(data)

    def get_param(self):
        """ GET new Parameters """
        return self.param

    def del_param(self, item):
        """ Deleting Parameters """
        self.param.pop(item, None)

    def reset_param(self):
        """ Reset Parameters """
        self.param = {}

    # Body Operations
    def add_body(self, data):
        """ Adding to body """
        self.body = data

    def append_body(self, data):
        """ Appending to body """
        self.body.update(data)

    def get_body(self):
        """ GET in body """
        return self.body

    def del_body(self, item):
        """ Deletion of body """
        self.body.pop(item, None)

    def reset_body(self):
        """ Reseting of body """
        self.body = {}

    # Files Operation
    def add_files(self, data):
        """ Adding files """

        self.files = data

    def append_files(self, data):
        """ Appending files """
        self.files.update(data)

    def get_files(self):
        """  GET files"""
        return self.files

    def del_files(self, item):
        """  Deletion of files """
        self.files.pop(item, None)

    def reset_files(self):
        """ Reset of files """
        self.files = {}

    # Header Operation
    def add_header(self, data):
        """ Adding Header """
        self.header = data

    def append_header(self, data):
        """ Append header """
        self.header.update(data)

    def get_header(self):
        """ GET header """
        return self.header

    def del_header(self, item):
        """ Deleting Header"""
        self.header.pop(item, None)

    def reset_header(self):
        """ Reset header """
        self.header = {'Content-Type': "application/json"}

    def add_proxy(self, **kwargs):
        """ Adding Proxy """
        self.header = kwargs

    def append_proxy(self, **kwargs):
        """ Appending a proxy """
        self.header.update(kwargs)

    def get_proxy(self):
        """ GET proxy """
        return self.header

    def del_proxy(self, item):
        """ Deletion of proxy """
        self.header.pop(item, None)

    def reset_proxy(self):
        """ Reseting Proxy """
        self.proxy = {}

    def reset(self):
        """
        Reset all, useful if same object is used to hit another API
        """
        self.param = {}
        self.header = {'Content-Type': "application/json"}
        self.proxy = {}
        self.body = {}
        self.files = {}
        self.request_type = "raw"
        self.basic_auth = ""
        self.add_basic_auth(VariablesDictionary.get_global_variable("username", ""),
                            VariablesDictionary.get_global_variable("password", ""))

    # METHODS:  GET/POST/PUT/DELETE

    def get(self, url):
        """  Used for GET Requests """
        url = "{}://{}:{}/{}".format(VariablesDictionary.get("protocol", "https"),
                                     VariablesDictionary.get("dut", "localhost"),
                                     VariablesDictionary.get("port", 80), url)
        try:
            if self.basic_auth != "":
                self.header["Authorization"] = self.basic_auth
            else:
                # If the header was already added and then deleted via function
                self.header.pop("Authorization", None)
            ssl_verify = VariablesDictionary.get_global_variable("verify_ssl", False)
            response = requests.get(
                url, headers=self.header, params=self.param, proxies=self.proxy,
                verify=ssl_verify, timeout=60)
            if response.status_code != 200:
                res = RestResponse({
                    "endpointinfo": {
                        "url": url,
                        "params": self.param,
                        "headers": self.header,
                        "proxy": self.proxy,
                        "requestType": self.request_type
                    },
                    "status": 'failure',
                    "message": "Request Code {}".format(response.status_code),
                    "err_code": 1001,
                    "response_code": response.status_code,
                    "data": None
                })
                self.reset()
                return res
            else:
                res = RestResponse({
                    "endpointinfo": {
                        "url": url,
                        "params": self.param,
                        "headers": self.header,
                        "proxy": self.proxy,
                    },
                    "status": 'success',
                    "message": "None",
                    "err_code": 0,
                    "data": response.text,
                    "response_code": response.status_code
                })
                self.reset()
                return res
        except Exception as e:
            res = RestResponse({
                "endpointinfo": {
                    "url": url,
                    "params": self.param,
                    "headers": self.header,
                    "proxy": self.proxy,
                },
                "status": 'failure',
                "message": "Unable to Reach Endpoint.",
                "err_code": 1002,
                "data": None,
                "response_code": -1
            })
            self.reset()
            return res

    def post(self, url):
        """
        Post Requests
        """
        url = "{}://{}:{}/{}".format(VariablesDictionary.get_global_variables_dictionary("protocol", "https"),
                                     VariablesDictionary.get("dut", "localhost"),
                                     VariablesDictionary.get("port", 80), url)
        try:
            if self.basic_auth != "":
                self.header["Authorization"] = self.basic_auth
            else:
                self.header.pop("Authorization", None)
            body = self.body
            # before sending the data in params, it should be in dict type
            if self.request_type == "raw" and not self.files:
                body = json.dumps(body)
            ssl_verify = VariablesDictionary.get("verify_ssl", False)
            response = requests.post(
                url, headers=self.header, params=self.param, data=body,
                proxies=self.proxy, verify=ssl_verify,
                timeout=60, files=self.files)
            if response.status_code != 200:
                res = RestResponse({
                    "endpointinfo": {
                        "url": url,
                        "params": self.param,
                        "headers": self.header,
                        "proxy": self.proxy,
                        "requestType": self.request_type,
                        "body": body
                    },
                    "status": 'failure',
                    "message": "Request Code {}".format(response.status_code),
                    "err_code": 1001,
                    "response_code": response.status_code,
                    "data": None
                })
                self.reset()
                return res
            else:
                res = RestResponse({
                    "endpointinfo": {
                        "url": url,
                        "params": self.param,
                        "headers": self.header,
                        "proxy": self.proxy,
                        "requestType": self.request_type,
                        "body": body
                    },
                    "status": 'success',
                    "message": "None",
                    "err_code": 0,
                    "data": response.text,
                    "response_code": response.status_code
                })
                self.reset()
                return res
        except Exception as e:
            res = RestResponse({
                "endpointinfo": {
                    "url": url,
                    "params": self.param,
                    "headers": self.header,
                    "proxy": self.proxy,
                    "requestType": self.request_type,
                    "body": body
                },
                "status": 'failure',
                "message": "Unable to Reach Endpoint {}".format(e),
                "err_code": 1002,
                "response_code": -1,
                "data": None
            })
            self.reset()
            return res

    def put(self, url):
        """
        PUT Requests
        """

        url = "{}://{}:{}/{}".format(variables_dictionary.get("protocol", "https"),
                                     variables_dictionary.get("dut", "localhost"),
                                     variables_dictionary.get("port", 80), url)
        body = self.body
        try:

            if self.basic_auth != "":
                self.header["Authorization"] = self.basic_auth
            else:
                # If the header was already added and then deleted via function
                self.header.pop("Authorization", None)
            if self.request_type == "raw" and not self.files:
                body = json.dumps(body)
            ssl_verify = variables_dictionary.get("verify_ssl", False)
            response = requests.put(
                url, headers=self.header, params=self.param, data=body,
                proxies=self.proxy, verify=ssl_verify,
                timeout=60, files=self.files)
            if response.status_code != 200:
                res = RestResponse({
                    "endpointinfo": {
                        "url": url,
                        "params": self.param,
                        "headers": self.header,
                        "proxy": self.proxy,
                        "requestType": self.request_type,
                        "body": body
                    },
                    "status": 'failure',
                    "message": "Request Code {}".format(response.status_code),
                    "err_code": 500,
                    "data": None,
                    "response_code": response.status_code
                })
                self.reset()
                return res
            else:
                res = RestResponse({
                    "endpointinfo": {
                        "url": url,
                        "params": self.param,
                        "headers": self.header,
                        "proxy": self.proxy,
                        "requestType": self.request_type,
                        "body": body
                    },
                    "status": 'success',
                    "message": "None",
                    "err_code": 0,
                    "data": response.text,
                    "response_code": response.status_code
                })
                self.reset()
                return res
        except Exception as e:
            res = RestResponse({
                "endpointinfo": {
                    "url": url,
                    "params": self.param,
                    "headers": self.header,
                    "proxy": self.proxy,
                    "requestType": self.request_type,
                    "body": body
                },
                "status": 'failure',
                "message": "Unable to Reach Endpoint",
                "err_code": 500,
                "data": None,
                "response_code": -1
            })
            self.reset()
            return res

    def delete(self, url):
        """
        Delete Requests
        """
        url = "{}://{}:{}/{}".format(variables_dictionary.get("protocol", "https"),
                                     variables_dictionary.get("dut", "localhost"),
                                     variables_dictionary.get("port", 80), url)
        try:
            body = self.body
            if self.basic_auth != "":
                self.header["Authorization"] = self.basic_auth
            else:
                # If the header was already added and then deleted via function
                self.header.pop("Authorization", None)
            if self.request_type == "raw":
                body = json.dumps(body)
            ssl_verify = variables_dictionary.get("verify_ssl", False)
            response = requests.delete(
                url, headers=self.header, params=self.param, data=body,
                proxies=self.proxy, verify=ssl_verify,
                timeout=60)
            if response.status_code != 200:
                res = RestResponse({
                    "endpointinfo": {
                        "url": url,
                        "param": self.param,
                        "header": self.header,
                        "proxy": self.proxy,
                        "requestType": self.request_type,
                        "body": body
                    },
                    "status": 'failure',
                    "message": "Request Code {}".format(response.status_code),
                    "err_code": 1001,
                    "response_code": response.status_code,
                    "data": None
                })
                self.reset()
                return res
            else:
                res = RestResponse({
                    "endpointinfo": {
                        "url": url,
                        "params": self.param,
                        "headers": self.header,
                        "requestType": self.request_type,
                        "proxy": self.proxy,
                        "body": body
                    },
                    "status": 'success',
                    "message": "None",
                    "err_code": 0,
                    "data": response.text,
                    "response_code": response.status_code
                })
                self.reset()
                return res
        except Exception as e:
            res = RestResponse({
                "endpointinfo": {
                    "url": url,
                    "params": self.param,
                    "headers": self.header,
                    "proxy": self.proxy,
                    "requestType": self.request_type,
                    "body": body
                },
                "status": 'failure',
                "message": "Unable to Reach Endpoint",
                "err_code": 1002,
                "data": None,
                "response_code": -1
            })
            self.reset()
            return res


class RestResponse:
    """
    Rest Response
    """
    def __init__(self, response):
        self.request_info = response['endpointinfo']
        self.status = response["status"]
        self.message = response["message"]
        self.error_code = response["err_code"]
        self.data = response["data"]
        self.res_code = response["response_code"]

    def get_JSONResponse(self):
        """ Get json response for response data."""
        return json.loads(self.data)

    def get_request_info(self):
        """ Get request info. """
        return self.request_info

    def get_error_code(self):
        """ Get error code. """
        return self.error_code

    def get_message(self):
        """ Get response message. """
        return self.message

    def get_data(self):
        """ Get response data. """
        return self.data

    def get_res_code(self):
        """ Get response code. """
        return self.res_code

    def get_status(self):
        """ Get status of response. """
        return self.status