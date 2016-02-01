from unittest import TestCase
from pipeline import pipeline_node, PipelineNode


class TestPipelineNode(TestCase):
    def test_create_nodes_using_classes(self):
        def func():
            pass

        func_node = PipelineNode(func)
        self.assertIsNotNone(func_node.neighbors)
        self.assertIsNotNone(func_node.connect)

    def test_create_nodes_using_decorators(self):
        @pipeline_node
        def func():
            pass

        self.assertIsNotNone(func.neighbors)
        self.assertIsNotNone(func.connect)

    def test_connected_nodes_are_pipelines(self):
        def a():
            pass

        def b():
            pass

        node_a = PipelineNode(a)
        node_b = PipelineNode(b)
        node_a.connect(node_b)
        self.assertIn(node_b, node_a.neighbors)


