import unittest
import queue
import multiprocessing
from dummy_functions import count, increment, save_to
from process_pipeline_factory import ProcessPipelineFactory
from thread_pipeline_factory import ThreadPipelineFactory

ONE_TO_TEN = list(range(1, 11))


class TestPipelineExecution(unittest.TestCase):
    def setUp(self):
        count.neighbors = []
        increment.neighbors = []

    def test_pipelines_can_be_executed_in_threads(self):
        t_queue = queue.Queue()
        count.connect(increment)
        increment.connect(save_to(t_queue))
        t_pype = ThreadPipelineFactory()
        t_pype.run_pipeline(count)
        result = []
        while len(result) < count.until:
            result.append(t_queue.get())
        self.assertEqual(result, ONE_TO_TEN)

    def test_pipelines_can_be_executed_in_processes(self):
        p_queue = multiprocessing.Queue()
        count.connect(increment)
        increment.connect(save_to(p_queue))
        p_pype = ProcessPipelineFactory()
        p_pype.run_pipeline(count)
        result = []
        while len(result) < count.until:
            result.append(p_queue.get())
        self.assertEqual(result, ONE_TO_TEN)
