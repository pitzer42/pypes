from queue import Queue
from random import random
from time import sleep
from threading import Thread
import inspect
import collections


class Pipeline:
    STOP = StopIteration()
    MAX_SLEEP_SECONDS = 0.01

    @classmethod
    def make_pipe(cls):
        return Queue()

    @classmethod
    def sleep_filter(cls):
        sleep(random() * Pipeline.MAX_SLEEP_SECONDS)

    def __init__(self):
        self.src = None
        self.snk = None
        self.filters = []
        self._last_output = None

    def source(self, func, output=None):
        if not output:
            output = Pipeline.make_pipe()
        self.src = Source(func)
        self.filters.insert(0, self.src)
        self._last_output = self.src.output = output

    def seq(self, func, output=None):
        if not output:
            output = Pipeline.make_pipe()
        func = Filter(func)
        func.input = self._last_output
        self._last_output = func.output = output
        self.filters.append(func)

    def par(self, output=None, *funcs):
        if not output:
            output = Pipeline.make_pipe()
        for func in funcs:
            func = Filter(func)
            func.input = self._last_output
            func.output = output
            self.filters.append(func)
        self._last_output = output

    def sink(self, func):
        self.snk = Sink(func)
        self.filters.append(self.snk)
        self.snk.input = self._last_output

    def start(self):
        for item in self.filters:
            item.start()


class Source(Thread):
    def __init__(self, func):
        Thread.__init__(self)
        self.output = None
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def run(self):
        for token in self.func():
            self.output.put(token)
            Pipeline.sleep_filter()


class Filter(Thread):
    def __init__(self, func):
        Thread.__init__(self)
        self.input = None
        self.output = None
        self.func = func
        # number of tokens popped from the input buffer each time
        self.n_args = len(inspect.getargspec(func).args)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def run(self):
        tokens = iter(self.input.get, Pipeline.STOP)
        args = []
        for token in tokens:
            if isinstance(token, collections.Iterable):
                args.extend(token)
            else:
                args.append(token)
            if len(args) == self.n_args:
                result = self.func(*args)
                self.output.put(result)
                args = []
            Pipeline.sleep_filter()
        self.output.put(Pipeline.STOP)
        # Put the STOP flag back to input for other filters
        self.input.put(Pipeline.STOP)


class Sink(Thread):
    def __init__(self, func):
        Thread.__init__(self)
        self.input = None
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def run(self):
        tokens = iter(self.input.get, Pipeline.STOP)
        for token in tokens:
            self.func(token)
            Pipeline.sleep_filter()
