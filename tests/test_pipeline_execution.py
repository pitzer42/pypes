import unittest
from pipeline import pipeline_node, PipelineNode, execute_threads, execute_processes

numbers = []


@pipeline_node
def count():
    for i in range(10):
        yield i


@pipeline_node
def increment(i):
    return i + 1


@pipeline_node
def save(i):
    numbers.append(i)


count.connect(increment)
increment.connect(save)


class TestPipelineExecution(unittest.TestCase):
    def setUp(self):
        self.numbers = []

    def test_pipelines_can_be_executed_in_threads(self):
        execute_threads(count)
        while len(numbers) < 10:
            pass
        one_until_ten = list(range(1, 11))
        self.assertEqual(numbers, one_until_ten)

    #TODO: replace numbers list by multiprocess.Queue
    def skip_test_pipelines_can_be_executed_in_threads(self):
        execute_processes(count)
        while len(numbers) < 10:
            pass
        one_until_ten = list(range(1, 11))
        self.assertEqual(numbers, one_until_ten)
