import time
import uuid

import requests

from pysurge import TestCase


class ExampleTest(TestCase):
    @classmethod
    def startup(cls):
        # A single requests session will be used for all tests fired in a
        # child process' thread pool
        cls.session = requests.Session()

    @classmethod
    def shutdown(cls):
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create a unique request ID to send as a header so we can track the requests
        # on the server side.
        self.request_id = str(uuid.uuid4())
        # Allow for a kwarg called 'path' to be specified which changes the URL that this
        # test will send requests to.
        self.path = str(kwargs.get("path", ""))
        # Allow for a kwarg that defines the base url
        self.url = kwargs.get("url", "http://localhost:80")

    @property
    def summary(self):
        # A brief summary of this test -- used in logging and report printing
        return "example test"

    @property
    def description(self):
        # A brief description of this test -- used in logging -- usually useful to include
        # "unique identifiers" in the test to help when analyzing logs.
        return f"example test: request id {self.request_id}"

    @property
    def max_duration(self):
        # How long we think each test instance takes to run at a maximum
        return 180

    def setup(self):
        pass

    def teardown(self):
        pass

    def run(self):
        headers = {"request-id": self.request_id}
        start_time = time.time()
        r = self.session.get(f"{self.url}/{self.path}", headers=headers)
        end_time = time.time()
        # A metric called 'response_time' is stored for each test.
        self.metrics["response_time"] = end_time - start_time
        # If the test hits an exception, it will be marked as a failure.
        r.raise_for_status()
