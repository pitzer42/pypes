import time
import collections
import inspect
from queue import Queue
from threading import Thread
from random import random

from parallel_pipeline_factory import ParallelPipelineFactory


class ThreadPipelineFactory(ParallelPipelineFactory):
    """
    Execute a pipeline with threads. If you are using cpython interpreter this only benefits IO bound pipelines.
    See https://wiki.python.org/moin/GlobalInterpreterLock
    :param src: root node
    """

    def create_buffer(self):
        return Queue()

    def create_source(self, func):
        return Source(func)

    def create_filter(self, func):
        return Filter(func)

    def create_sink(self, func):
        return Sink(func)


class Source(Thread):
    def __init__(self, func):
        Thread.__init__(self)
        self.func = func
        self.out_buffer = None

    def run(self):
        for token in self.func():
            self.out_buffer.put(token)
            sleep()
        self.out_buffer.put(STOP_FLAG)


class Filter(Thread):
    def __init__(self, func):
        Thread.__init__(self)
        self.in_buffer = None
        self.out_buffer = None
        self.func = func
        # number of tokens popped from the input buffer each time
        self.n_args = len(inspect.getargspec(func).args)

    def run(self):
        args = []
        tokens = iter(self.in_buffer.get, STOP_FLAG)
        for token in tokens:
            if isinstance(token, collections.Iterable):
                args.extend(token)
            else:
                args.append(token)
            if len(args) == self.n_args:
                result = self.func(*args)
                self.out_buffer.put(result)
                args = []
            sleep()
        # Put the STOP flag back to input for other filters
        self.in_buffer.put(STOP_FLAG)
        self.out_buffer.put(STOP_FLAG)


class Sink(Thread):
    def __init__(self, func):
        Thread.__init__(self)
        self.in_buffer = None
        self.func = func

    def run(self):
        tokens = iter(self.in_buffer.get, STOP_FLAG)
        for token in tokens:
            self.func(token)
            sleep()


STOP_FLAG = StopIteration()
MAX_SLEEP_SECONDS = 0.0001


def sleep():
    time.sleep(random() * MAX_SLEEP_SECONDS)
