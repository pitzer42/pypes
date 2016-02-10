from dummy_functions import count, increment
from unittest import TestCase
from nodes import PipelineNode


class TestNodes(TestCase):
    def test_create_nodes_using_classes(self):
        func_node = PipelineNode(count)
        self.assertIsNotNone(func_node.neighbors)
        self.assertIsNotNone(func_node.connect)

    def test_create_nodes_using_decorators(self):
        self.assertIsNotNone(count.neighbors)
        self.assertIsNotNone(count.connect)

    def test_connected_nodes_are_pipelines(self):
        node_a = PipelineNode(count)
        node_b = PipelineNode(increment)
        node_a.connect(node_b)
        self.assertIn(node_b, node_a.neighbors)
