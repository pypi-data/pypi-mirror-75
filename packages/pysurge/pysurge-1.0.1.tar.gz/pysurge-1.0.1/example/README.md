# `pysurge` example

Let's say you want to write a simple performance test that sends HTTP GET requests to a web server at a certain rate. This example demonstrates how easily this can be accomplished.

The test scenario that we want to run at scale is written in a class like so:

```python
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
```

A configuration file is then created to run two iterations of this test: one which sends GET requests to "/" and one which sends GET requests to "/badpath":

```yaml
tests:
- test_class: example_test.ExampleTest
  kwargs:
    url: http://localhost:80
    path: badpath  # this test will repeatedly send a request to a bad url
  rate: 0.2  # number of tests fired per second ... 0.2 = 1 test every 5 sec
- test_class: example_test.ExampleTest
  kwargs:
    url: http://localhost:80
  rate: 0.2
  ```


Now, start up a local httpbin server with docker:
```
docker run -p 80:80 -e GUNICORN_CMD_ARGS="--capture-output --error-logfile - --access-logfile - --access-logformat '%(h)s %(t)s %(r)s %(s)s Host: %({Host}i)s}'" kennethreitz/httpbin
```

The additional gunicorn arguments will cause logs to be displayed to stdout for incoming HTTP requests.


Run `pysurge` for 1 minute with:
```
pysurge -c example_config.yml -d 1
```

By default, `pysurge` only logs an error when a test fails. If you wish to see more information then you can enable debug mode:
```
pysurge -c example_config.yml -d 1 --debug
```

Looking at the logs of the `httpbin` server, we can see requests coming in for each test every 5 seconds:
```
172.17.0.1 [06/Jul/2020:22:16:54 +0000] GET /badpath HTTP/1.1 404 Host: localhost}
172.17.0.1 [06/Jul/2020:22:16:56 +0000] GET / HTTP/1.1 200 Host: localhost}
172.17.0.1 [06/Jul/2020:22:16:59 +0000] GET /badpath HTTP/1.1 404 Host: localhost}
172.17.0.1 [06/Jul/2020:22:17:02 +0000] GET /badpath HTTP/1.1 404 Host: localhost}
172.17.0.1 [06/Jul/2020:22:17:04 +0000] GET / HTTP/1.1 200 Host: localhost}
172.17.0.1 [06/Jul/2020:22:17:07 +0000] GET /badpath HTTP/1.1 404 Host: localhost}
172.17.0.1 [06/Jul/2020:22:17:09 +0000] GET / HTTP/1.1 200 Host: localhost}
172.17.0.1 [06/Jul/2020:22:17:12 +0000] GET / HTTP/1.1 200 Host: localhost}
172.17.0.1 [06/Jul/2020:22:17:14 +0000] GET /badpath HTTP/1.1 404 Host: localhost}
172.17.0.1 [06/Jul/2020:22:17:17 +0000] GET / HTTP/1.1 200 Host: localhost}
172.17.0.1 [06/Jul/2020:22:17:19 +0000] GET /badpath HTTP/1.1 404 Host: localhost}
```
