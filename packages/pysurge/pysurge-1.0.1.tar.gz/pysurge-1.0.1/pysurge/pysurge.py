import logging
import multiprocessing
import os
import queue
import signal
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pydoc import locate


log = logging.getLogger(__name__)


class TestCase:
    """
    Base class for a test case that is run by the perf tester

    Any TestCase should implement the below methods.
    """

    @classmethod
    def startup(cls):
        """Defines session-level startup work that applies to all tests of this same type.

        Anything stored here will be a class attr and therefore accessible to
        all the instances of the test that are kicked off by TestRunner

        TestRunner will run this before starting load.

        Even if you run multiple instances of the same test (but with different
        kwargs), the startup will run only ONCE per test class in each child
        process.
        """
        raise NotImplementedError

    @classmethod
    def shutdown(cls):
        """Defines session-level shutdown work that applies to all tests of this same type.

        TestRunner will run this after load runs stop.
        """
        raise NotImplementedError

    def __init__(self, **kwargs):
        """Define any attrs you want to store at instantiation.

        Note that this should not be confused with self.setup() below. The
        main usage for self.__init__ would be to initialize any kwarg vars that
        relate to your test case's "configuration". For example, a parameter
        or a boolean.

        The kwargs are configured in the perf test YAML configuration.
        """
        super().__init__()
        self.kwargs = kwargs
        # Metrics is a dict with arbitrary keys, with values of ints/float that a TestCase can save
        # for each test run. The recorded values are averaged at the end of the run for reporting
        # purposes
        #
        # A metric is only counted towards the average when a test *passes*
        self.metrics = {}

    def __str__(self):
        return f"<{self.__class__.__name__} kwargs={self.kwargs}>"

    @property
    def summary(self):
        """Return a short summary of what this test does (for reporting purposes)."""
        raise NotImplementedError

    @property
    def description(self):
        """Returns a description for this specific test case (string)

        Since the description is used by TestRunner for logging purposes,
        the description should only depend on attrs defined in self.__init__,
        self.startup, and self.shutdown
        """
        raise NotImplementedError

    @property
    def max_duration(self):
        """Returns the maximum time in sec that an instance of this test may take to run"""
        raise NotImplementedError

    def setup(self):
        """Defines setup for a single execution of this test."""
        raise NotImplementedError

    def teardown(self):
        """Defines teardown for a single execution of this test."""
        raise NotImplementedError

    def run(self):
        """Defines the procedure to actually run the test.

        Any Exception raised in here will be marked as a test failure by TestRunner.
        """
        raise NotImplementedError


class TestRunner:
    """
    Runs a TestCase at a specific rate in a thread pool and keeps track of successes/failures

    Args:
        test_cls: The TestCase test to run
        rate (float): The rate to run test_cls at, in # of tests/per sec
    """

    def __init__(self, test_cls, test_cls_kwargs, rate, debug=False):
        self._stop = threading.Event()
        self._stop.set()
        self._lock = threading.Lock()
        self.test_cls = test_cls
        self.test_cls_kwargs = test_cls_kwargs
        self.test_instance = test_cls(**test_cls_kwargs)
        self.rate = rate  # num tests per sec
        self.active_tests = 0
        self.successes = 0
        self.failures = 0
        self.test_run_time = 0
        self.metrics = {}
        self.debug = debug

    @property
    def running(self):
        return not self._stop.is_set() or self.active_tests > 0

    def _test_runner(self):
        """Runs a single test in a thread, stores results."""
        with self._lock:
            self.active_tests += 1

        try:
            test = self.test_cls(**self.test_cls_kwargs)
            log.debug("test '%s' in setup()", test.description)
            test.setup()
            log.debug("test '%s' in run()", test.description)
            test.run()

            with self._lock:
                for metric, value in test.metrics.items():
                    if metric not in self.metrics:
                        self.metrics[metric] = []
                    self.metrics[metric].append(value)
                    log.debug(
                        "test '%s' storing metric '%s' value '%f'", test.description, metric, value
                    )
                self.successes += 1
                log.debug("test '%s' passed", test.description)
        except Exception as exc:
            log.error("test '%s' hit error: %s", test.description, str(exc))
            with self._lock:
                self.failures += 1
            if self.debug:
                raise
        finally:
            try:
                log.debug("test '%s' in teardown()", test.description)
                test.teardown()
            except Exception as exc:
                log.exception("test '%s' hit error in teardown: %s", test.description, str(exc))
            finally:
                with self._lock:
                    self.active_tests -= 1

    def stop(self):
        """Trigger tests to stop and finish up."""
        if self._stop.is_set():
            return

        log.info(
            "TestRunner stopping for %s... %d active threads need to finish",
            str(self.test_cls),
            self.active_tests,
        )
        self._stop.set()

    def _thread_pool_submitter(self):
        """Handles the continuous loop to submit tests to the thread pool executor."""
        start_time = time.time()

        max_duration = self.test_instance.max_duration
        # Based on Little's Law
        # Max number of concurrent tests = (num tests fired/sec) * (max duration in sec of test)
        workers = self.rate * max_duration

        executor = ThreadPoolExecutor(max_workers=workers)

        rate_of_fire = 1.0 / self.rate  # 1 test fired every 'rate_of_fire' seconds

        while not self._stop.is_set():
            try:
                executor.submit(self._test_runner)
            except RuntimeError as err:
                if "can't start new thread" in str(err):
                    log.error("unable to start new thread! desired rate won't be achieved")
                else:
                    raise

            time.sleep(rate_of_fire)

        executor.shutdown()

        stop_time = time.time()
        self.test_run_time = stop_time - start_time

    def run(self):
        """
        Start running tests at the defined rate.

        Starts a thread that takes care of submitting tests to a thread pool, so
        this is a non-blocking call.
        """
        self.successes = 0
        self.failures = 0
        self._stop.clear()

        t = threading.Thread(target=self._thread_pool_submitter)
        t.daemon = True
        t.start()


class ChildProcess(multiprocessing.Process):
    """
    A child process which runs multiple TestRunner instances.

    One ChildProcess runs per CPU on the machine executing load tests. The total amount of tests
    running for each test case is spread across all the ChildProcesses by adjusting their rate:
    child process rate = total rate / # processors
    """

    @staticmethod
    def _test_cls_shutdown(test_cls):
        """Run shutdown for a test_cls and log any exception."""
        try:
            log.debug("test class %s calling shutdown()", test_cls.__name__)
            test_cls.shutdown()
            return True
        except Exception:
            log.exception("Warning: shutdown for %s failed.", str(test_cls))
            return False

    @staticmethod
    def _test_cls_startup(test_cls):
        """Run the startup for a test_cls and log any exception."""
        try:
            log.debug("test class %s calling startup()", test_cls.__name__)
            test_cls.startup()
            return True
        except Exception:
            log.exception("Startup for %s failed! Not running this test.", str(test_cls))
            return False

    def __init__(
        self, config, run_start_delay, start_event, stop_event, result_queue, proc_num, debug=False
    ):
        self.config = config
        self.proc_run_start_delay = run_start_delay
        self.start_event = start_event
        self.stop_event = stop_event
        self.result_queue = result_queue
        self.perf_testers = []
        self.processors = multiprocessing.cpu_count()
        self.startup_attempted = []
        self.startup_successful = []
        self.proc_num = proc_num
        self.debug = debug
        super().__init__()

    def _stop_and_send_results(self):
        """
        Stop all perf testers and wait for them to complete

        Results are then pushed onto the result queue.

        TODO: in future results may be pushed concurrently in real time to a 'reporter'
        """
        for perf_tester in self.perf_testers:
            perf_tester.stop()
        while any([pt.running for pt in self.perf_testers]):
            time.sleep(1)

        for test_cls in self.startup_attempted:
            self._test_cls_shutdown(test_cls)

        results = []
        for pt in self.perf_testers:
            # Instantiate the test class w/ kwargs so we can get the unique name/summary properties
            test = pt.test_instance
            test_name = f"{str(test)} -- {test.summary}"
            results.append(
                {
                    "test_name": test_name,
                    "successes": pt.successes,
                    "failures": pt.failures,
                    "metrics": pt.metrics,
                }
            )
        self.result_queue.put(results)

    def _init_test_runners(self):
        # Run startup once per test class
        for test_config in self.config["tests"]:
            test_cls = test_config["test_class"]
            if test_cls not in self.startup_attempted:
                if self._test_cls_startup(test_cls):
                    self.startup_successful.append(test_cls)
                self.startup_attempted.append(test_cls)

        total_rate_this_proc = 0.0

        # Run only the test classes that passed startup successfully
        for test_config in self.config["tests"]:
            rate_per_proc = test_config["rate"] / self.processors
            test_cls = test_config["test_class"]
            test_kwargs = test_config.get("kwargs", {})
            if test_cls in self.startup_successful:
                pt = TestRunner(test_cls, test_kwargs, rate_per_proc, self.debug)
                self.perf_testers.append(pt)
                total_rate_this_proc += pt.rate

        return total_rate_this_proc

    def run(self):
        """
        The logic running within each child process.

        Takes care of:
        1. running session startup for each test case class
        2. launching a TestRunner for that TestCase
        3. initiating the start of the TestRunners (only if their startup worked)
        4. trigger stop of the TestRunners
        5. running session shutdown for each test case class
        6. sending results back to the main process on result_queue
        """
        signal.signal(signal.SIGINT, signal.SIG_IGN)  # worker procs ignore sigint

        try:
            total_rate_this_proc = self._init_test_runners()
        except Exception:
            log.exception("Child process hit error during startup")
            self.result_queue.put("STARTUP_FAILED")
            return

        log.info("Sending 'startup done' to main proc and waiting for it to tell me to start...")
        self.result_queue.put("STARTUP_DONE")

        self.start_event.wait()

        # Wait for instruction from the main proc to start firing tests
        if len(self.startup_successful) < 1:
            log.error(
                "No tests to run on this child process... startup likely failed on all of them"
            )
        else:
            log.info("Sleeping for proc start delay: %f", self.proc_run_start_delay)
            time.sleep(self.proc_run_start_delay)
            log.info("Done sleeping")

            # Stagger the start of the perf testers within this proc to more evenly space test fires
            # Also shuffle the order in which they start
            if self.proc_num % 2:
                perf_testers = reversed(self.perf_testers)
            else:
                perf_testers = self.perf_testers
            for count, pt in enumerate(perf_testers):
                delay = (1 / total_rate_this_proc) * count
                time.sleep(delay)
                pt.run()
            # Wait until trigger to stop is received
            self.stop_event.wait()

        self._stop_and_send_results()


class Manager:
    """Handles running multiple TestRunners, splitting them across ChildProcesses."""

    @staticmethod
    def _validate_test_cls(test_cls, test_cls_kwargs):
        instance = test_cls(**test_cls_kwargs)

        try:
            instance.max_duration
        except NotImplementedError:
            raise AttributeError(
                f"{type(instance)} must have max_duration property defined"
            ) from None  # avoid printing the original chained error

    def __init__(self, config, duration, debug=False):
        # TODO: real config management
        self.config = config
        self.processors = multiprocessing.cpu_count()  # integer value
        self.result_queue = multiprocessing.Queue()
        self.start_event = multiprocessing.Event()
        self.stop_event = multiprocessing.Event()
        self.start_time = 0.0
        self.stop_time = 0.0
        self.duration = duration
        self.debug = debug

        # Append cwd to sys.path so we can load adhoc test classes
        sys.path.insert(0, os.getcwd())

        # Map the test class string in the config into an actual imported class
        log.info("Validating test classes...")
        for test in self.config["tests"]:
            test_cls = test["test_class"]
            test_cls_kwargs = test.get("kwargs", {})
            imported_cls = locate(test_cls)
            if not imported_cls:
                raise ValueError(f"Unable to import test class '{test_cls}'")
            test["test_class"] = imported_cls
            self._validate_test_cls(imported_cls, test_cls_kwargs)

        # Remove freshly added cwd from path
        sys.path.pop(0)

    def _aggregate_results(self, results):
        """Take the results returned by each proc and aggregate."""
        aggregated = {}

        # Aggregate all the values
        for result_list in results:
            for result in result_list:
                test_name = result["test_name"]
                successes = result["successes"]
                failures = result["failures"]
                metrics = result["metrics"]

                if test_name not in aggregated:
                    aggregated[test_name] = {
                        "successes": 0,
                        "failures": 0,
                        "metrics": {},
                    }

                # Add up successes/failures
                aggregated[test_name]["successes"] += successes
                aggregated[test_name]["failures"] += failures

                # Aggregate metric values
                aggregated_metrics = aggregated[test_name]["metrics"]
                if successes > 0:
                    for metric, values in metrics.items():
                        if metric not in aggregated_metrics:
                            aggregated_metrics[metric] = values
                        else:
                            aggregated_metrics[metric] += values

        # Print aggregated results (and calc avg for each metric)
        for test_name, result in aggregated.items():
            successes = result["successes"]
            failures = result["failures"]
            metrics = result["metrics"]

            log.info("---- Results for test '%s' ----", test_name)
            log.info(
                ">>> Ran for %f sec, fired %d total tests",
                self.stop_time - self.start_time,
                successes + failures,
            )
            log.info(">>> Successes: %d, failures: %d", successes, failures)
            log.info("---- Metrics for test '%s' ----", test_name)
            for metric, values in metrics.items():
                log.info(">>> %s: %f", metric, sum(values) / len(values))
            log.info("\n\n")

    def stop(self):
        log.info("STOPPING -- Telling child processes to begin shutting down...")
        self.stop_event.set()
        self.stop_time = time.time()

    def _signal_handler(self, signal, frame):
        log.info("CTRL+C HIT -- stopping")
        self.stop()

    def start(self):
        """
        Start running the perf tests.

        They will run until the load run duration is reached, or until ctrl+C is pressed
        """
        # ctrl+C signal should set the stop event to trigger child procs to stop
        signal.signal(signal.SIGINT, self._signal_handler)

        self.child_procs = []

        self.start_event.clear()
        self.stop_event.clear()

        total_rate = sum([test_config["rate"] for test_config in self.config["tests"]])

        for count in range(0, self.processors):
            # stagger the start of each proc so they fire tests evenly spaced
            delay = (1 / total_rate) * count
            proc = ChildProcess(
                self.config,
                delay,
                self.start_event,
                self.stop_event,
                self.result_queue,
                count,
                self.debug,
            )
            proc.start()
            self.child_procs.append(proc)

        # wait for the 'startup' to finish
        results = []
        log.info("Waiting to receive 'startup done' from child procs...")
        failed = False
        while len(results) < len(self.child_procs):
            try:
                result = self.result_queue.get(block=False)
                if result == "STARTUP_FAILED":
                    log.debug("Startup for a child process failed")
                    failed = True
                elif result != "STARTUP_DONE":
                    log.debug("Expected a STARTUP_DONE result, got something else")
                    failed = True
                results.append(result)
            except queue.Empty:
                time.sleep(0.1)

        if failed:
            raise Exception("Startup of child processes failed")

        # Now trigger the actual run
        log.info("Starting...")
        self.start_time = time.time()
        self.start_event.set()

        if self.duration:
            time_to_stop = self.start_time + self.duration
        else:
            time_to_stop = None

        # Wait for the results from each proc to come in
        results = []
        while len(results) < len(self.child_procs):
            if time_to_stop and time.time() >= time_to_stop and not self.stop_event.is_set():
                self.stop()
            try:
                results.append(self.result_queue.get(block=False))
            except queue.Empty:
                time.sleep(0.1)

        if self.stop_time == 0.0:
            # There was some error and tests weren't stopped cleanly...
            self.stop_time = time.time()

        self._aggregate_results(results)
