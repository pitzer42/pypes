from thread_pipeline import thread_pipeline_from_graph
from process_pipeline import process_pipeline_from_graph


def pipeline_node(func):
    return PipelineNode(func)


class PipelineNode:
    def __init__(self, func):
        self.func = func
        self.neighbors = []

    def connect(self, *args):
        self.neighbors += args

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def execute_threads(src):
    threads = thread_pipeline_from_graph(src)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def execute_processes(src):
    processes = process_pipeline_from_graph(src)
    for process in processes:
        process.start()
    for process in processes:
        process.join()

