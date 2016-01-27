import time
import collections
import inspect
from multiprocessing import Process, Queue
from random import random


def process_pipeline_from_graph(src):
    node_to_process = {src: Source(src)}
    working = [src]
    while len(working) > 0:
        node = working.pop()
        node_p = node_to_process[node]
        for neighbor in node.neighbors:
            if neighbor not in node_to_process:
                node_to_process[neighbor] = create_process(neighbor)
                working.append(neighbor)
            neighbor_p = node_to_process[neighbor]
            connect_buffers(node_p, neighbor_p)
    return node_to_process.values()


def create_process(n):
    if len(n.neighbors) > 0:
        return Filter(n)
    return Sink(n)


def connect_buffers(a, b):
    if a.out_buffer is None and b.in_buffer is None:
        a.out_buffer = b.in_buffer = default_pipe()
    elif b.in_buffer is None:
        b.in_buffer = a.out_buffer
    else:
        a.out_buffer = b.in_buffer


class Source(Process):
    def __init__(self, func):
        Process.__init__(self)
        self.func = func
        self.out_buffer = None

    def run(self):
        for token in self.func():
            self.out_buffer.put(token)
            sleep()
        self.out_buffer.put(STOP_FLAG)


class Filter(Process):
    def __init__(self, func):
        Process.__init__(self)
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


class Sink(Process):
    def __init__(self, func):
        Process.__init__(self)
        self.in_buffer = None
        self.func = func

    def run(self):
        tokens = iter(self.in_buffer.get, STOP_FLAG)
        for token in tokens:
            self.func(token)
            sleep()


STOP_FLAG = StopIteration
MAX_SLEEP_SECONDS = 0.0001


def default_pipe():
    return Queue()


def sleep():
    time.sleep(random() * MAX_SLEEP_SECONDS)
