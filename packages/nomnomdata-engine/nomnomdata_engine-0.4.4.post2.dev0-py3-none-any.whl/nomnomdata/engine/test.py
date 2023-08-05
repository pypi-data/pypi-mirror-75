import json
import logging
import os
import re
from pprint import pformat

from httmock import HTTMock, urlmatch

from .logging import threadPool as loggingThreadPool


class NominodeMock(HTTMock):
    def __init__(self, task_parameters=None):
        super().__init__(self.api_match)
        self.logger = logging.getLogger("nomigen.nominode-mock")
        task_parameters = task_parameters or {}
        self.secrets = task_parameters.pop("config", {})
        self.params = task_parameters
        self.calls = []

    def __enter__(self):
        super().__enter__()
        self.old_environ = os.environ.copy()
        os.environ["execution_uuid"] = "TEST_UUID"
        os.environ["task_uuid"] = "TASK_UUID"
        os.environ["project_uuid"] = "TEST_PROJECT"
        os.environ["nomnom_api"] = "http://127.0.0.1:9090"
        os.environ["token"] = "token"
        return self

    def __exit__(self, type, value, traceback):
        # slight pause on exit to any loggers to finish up
        loggingThreadPool.shutdown()
        super().__exit__(type, value, traceback)
        os.environ.clear()
        os.environ.update(self.old_environ)

    @urlmatch(netloc=r"(.*\.)?127.0.0.1:9090$")
    def api_match(self, url, request):
        self.calls.append((url.path, json.loads(request.body)))
        match = re.match(r"/connection/(?P<uuid>.+)/update", url.path)
        if match:
            json_data = request.body
            loaded = json.loads(json_data)
            uuid = match.groupdict()["uuid"]
            self.params["config"][uuid] = json.loads(loaded["parameters"])
            self.logger.debug("Caught connections update. Test creds updated")
        elif url.path == "/execution/log/TEST_UUID":
            json_data = request.body
            loaded = json.loads(json_data)
        elif url.path == "/task/TASK_UUID/update":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug("Caught task update {}".format(pformat(loaded)))
        elif url.path == "/execution/update/TEST_UUID":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug(
                "Caught execution progress update {}".format(pformat(loaded))
            )
        elif url.path == "/execution/decode/TEST_UUID":
            return json.dumps(self.secrets)
        elif url.path == "/task/TASK_UUID/parameters":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug("Caught task parameter update {}".format(pformat(loaded)))
            return json.dumps({"result": "success"})
        elif url.path == "/execution/checkout/TEST_UUID":
            return json.dumps({"parameters": self.params, "task_uuid": "TASK_UUID"})
        else:
            self.logger.info(
                f"Unknown api endpoint called {url.path}, \n Body {request.body}"
            )
        return '{"you_logged":"test"}'
