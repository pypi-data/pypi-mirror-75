# `pysurge`

Have existing Python code? Want to use it to set up some simple performance tests quickly? Try `pysurge`, a python-based tool that allows you to quickly write simple performance tests in python.

### Example

See the [example](example) in this project to see how a simple HTTP load test can be quickly configured and executed.

### Installation

This project is available on pypi:

```
pip install pysurge
```

### Performance tests... in Python?

Yes, Python has its limitations when it comes to concurrency and scale. However, sometimes you don't need more scale than what Python can deliver. This is especially true when testing cloud-based applications that "scale out" (i.e., spin up more replicas when demand increases). Load testing can be done at lower scale against a single replica and results can be extrapolated.

There's a lot of complex performance test tools out there that are designed to load test applications at very high scale. This project aims to offer a "quick and easy" solution for those who don't need the massive scale. The scale you can achieve is of course limited by the demands of your test, python's concurrency drawbacks (i.e., the GIL), and your hardware's specifications (number of CPU cores being a key factor).

Many test engineers already have code written in Python. The goal of this project is to prevent engineers from having to significantly re-write their logic just to get it running at higher scale. If the code is thread-safe, it can be imported and executed concurrently using `pysurge`.

### How does `pysurge` work?


#### Writing a TestCase class

Tests are defined by the test writer to inherit from the `pysurge.TestCase` class with the following functions:
* `startup` & `shutdown` -- these define "per-session" setup and teardown tasks that will happen once per test case class. Here you can also define variables/functions/etc. that all the fired test instances will share.
* `setup` & `teardown` -- define the "per-test" setup and teardown tasks that are executed for every unique test instance that is fired off
* `run` -- defines the actual test run logic
* the `__init__` can also define custom kwargs -- useful if you want to tweak the behavior of the test slightly.


#### Test metrics


A test case class can store float/int metrics in a dict called `self.metrics`. For example, you may want to store a metric that tracks the "response time" of your service every time the test fires. In your test's `run` function, you may have code that looks something like this:

```
start_time = time.time()
do_stuff()
end_time = time.time()
self.metrics['response_time'] = end_time - start_time
```

At the end of the test run, the metric stored for every instance that fired is averaged together and reported.


#### Configuring the pysurge run

`pysurge` uses a YAML configuration file which defines:
* which test classes you want to run
* the rate (# of tests per sec) to fire them off at
* any kwargs that should be passed to the `TestCase.__init__` -- useful if you want to run the same test class concurrently but with different options

#### Initiating the run

You can initiate a test run with:
```
$ pysurge -c </path/to/config.yaml> -d <run duration in minutes>
```

#### What happens during the run?

To make use of thread pools as efficiently as possible, `pysurge` uses `multiprocessing` to create a child process for each CPU core available on your system. A threadpool is created for each `TestClass` within every child process, and the test "fire rate" is then distributed evenly across each child process. For example, if you define a test case called `MyTest` that should be fired "once every second", and you have 4 CPU cores, the following will happen:
* Four child processes will be created
* A threadpool will be created in each child process which runs the code from `MyTest`
* Each threadpool will fire the test at a rate of "1 every 4 sec"
* Each child process staggers the start of its test fires by 1 second to make the "firing rate" even.

Once the test run has "ramped up" and all thread pools have begun firing, this results in 1 instance of `MyTest` firing every 1 second.

As you add more test classes, more thread pools are added to each child process. The number of child processes will remain constant.

Since the tests are executed in thread pools, they cannot be overly CPU intensive -- ideal candidates are quicker I/O bound tests interacting with remote APIs/services. Tests should take care to use CPU resources efficiently -- i.e. focus on I/O bound tasks (like interacting with remote network services) and remember to 'sleep' while looping to avoid sucking up CPU cycles.


#### Stopping the run

You can send `SIGINT`/`ctrl+C` to end the run prematurely. This will NOT abruptly end the application, but rather it will trigger all child processes to begin shutting down cleanly. Otherwise, the run will execute for the `duration` specified at run time.

#### Viewing results

`pysurge` outputs logs from all running threads to `stdout`

It will also produce a rudimentary report at the end of its run.

The below example is for a test called `UploadTest`. Two instances of this test were configured to run:
* `UploadTest` with no kwargs
* `UploadTest` with kwargs `legacy=True`

A metric called `upload->db_time_in_sec` was stored every time the test fired. The average time is reported in the report.

```
2018-09-14 18:51:37,590 MainProcess MainThread INFO ---- Results for test '<UploadTest kwargs={}> -- upload test, legacy: False' ----
2018-09-14 18:51:37,590 MainProcess MainThread INFO >>> Ran for 1849.129022 sec, fired 6988 total tests
2018-09-14 18:51:37,590 MainProcess MainThread INFO >>> Successes: 6987, failures: 1
2018-09-14 18:51:37,591 MainProcess MainThread INFO ---- Metrics for test '<UploadTest kwargs={}> -- upload test, legacy: False' ----
2018-09-14 18:51:37,591 MainProcess MainThread INFO >>> upload->db_time_in_sec: 2.668292
2018-09-14 18:51:37,591 MainProcess MainThread INFO
2018-09-14 18:51:37,591 MainProcess MainThread INFO ---- Results for test '<UploadTest kwargs={'legacy': True}> -- upload test, legacy: True' ----
2018-09-14 18:51:37,591 MainProcess MainThread INFO >>> Ran for 1849.129022 sec, fired 7004 total tests
2018-09-14 18:51:37,591 MainProcess MainThread INFO >>> Successes: 7002, failures: 2
2018-09-14 18:51:37,591 MainProcess MainThread INFO ---- Metrics for test '<UploadTest kwargs={'legacy': True}> -- upload test, legacy: True' ----
2018-09-14 18:51:37,591 MainProcess MainThread INFO >>> upload->db_time_in_sec: 1.025963
2018-09-14 18:51:37,591 MainProcess MainThread INFO
```


### What does `pysurge` NOT do?

* Very large scale tests
* Distributed load testing (orchestrating and firing tests across multiple hosts)
* Advanced reporting
