import unittest
import queue
import multiprocessing
from pipeline import pipeline_node, PipelineNode, execute_threads, execute_processes
from test_functions import count, increment, save_to


class TestPipelineExecution(unittest.TestCase):
    def test_pipelines_can_be_executed_in_threads(self):
        numbers = queue.Queue()

        count_node = PipelineNode(count)
        increment_node = PipelineNode(increment)
        save_node = PipelineNode(save_to(numbers))

        count_node.connect(increment_node)
        increment_node.connect(save_node)

        execute_threads(count_node)

        while numbers.qsize() < 10:
            pass
        one_until_ten = list(range(1, 11))

        result = []
        while len(result) < 10:
            result.append(numbers.get())

        self.assertSequenceEqual(result, one_until_ten)

    def skip_test_pipelines_can_be_executed_in_threads(self):
        numbers = multiprocessing.Queue()

        count_node = PipelineNode(count)
        increment_node = PipelineNode(increment)
        save_node = PipelineNode(save_to(numbers))

        count_node.connect(increment_node)
        increment_node.connect(save_node)

        execute_processes(count_node)

        result = []
        while len(result) < 10:
            result.append(numbers.get())

        while numbers.qsize() < 10:
            pass
        one_until_ten = list(range(1, 11))
        self.assertSequenceEqual(result, one_until_ten)
