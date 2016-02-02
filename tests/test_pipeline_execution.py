import unittest
import queue
import multiprocessing
from pipeline import execute_threads, execute_processes
from test_functions import count, increment, save_to

one_until_ten = list(range(1, 11))


class TestPipelineExecution(unittest.TestCase):
    def setUp(self):
        count.neighbors = []
        increment.neighbors = []

    def test_pipelines_can_be_executed_in_threads(self):
        t_queue = queue.Queue()
        count.connect(increment)
        increment.connect(save_to(t_queue))
        execute_threads(count)
        result = []
        while len(result) < count.until:
            result.append(t_queue.get())
        self.assertEqual(result, one_until_ten)

    def test_pipelines_can_be_executed_in_processes(self):
        p_queue = multiprocessing.Queue()
        count.connect(increment)
        increment.connect(save_to(p_queue))
        execute_processes(count)
        result = []
        while len(result) < count.until:
            result.append(p_queue.get())
        self.assertEqual(result, one_until_ten)
