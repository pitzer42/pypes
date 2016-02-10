class ParallelPipelineFactory:
    """
    Execute a pipeline with processes. Benefits CPU bound pipelines
    :param src: root node
    """

    def __init__(self):
        pass

    def create_buffer(self):
        raise NotImplemented()

    def create_source(self, func):
        raise NotImplemented()

    def create_filter(self, func):
        raise NotImplemented()

    def create_sink(self, func):
        raise NotImplemented()

    def run_pipeline(self, root):
        parallel_units = self.create_pipeline_from_graph(root)
        for unit in parallel_units:
            unit.start()
        for unit in parallel_units:
            unit.join()

    def create_pipeline_from_graph(self, src):
        nodes_to_parallel_units = {src: self.create_source(src)}
        working = [src]
        while len(working) > 0:
            node = working.pop()
            node_parallel_unit = nodes_to_parallel_units[node]
            for neighbor in node.neighbors:
                if neighbor not in nodes_to_parallel_units:
                    if neighbor.has_neighbors():
                        nodes_to_parallel_units[neighbor] = self.create_filter(neighbor)
                    else:
                        nodes_to_parallel_units[neighbor] = self.create_sink(neighbor)
                    working.append(neighbor)
                neighbor_parallel_unit = nodes_to_parallel_units[neighbor]
                self.connect_buffers(node_parallel_unit, neighbor_parallel_unit)
        return nodes_to_parallel_units.values()

    def connect_buffers(self, a, b):
        if a.out_buffer is None and b.in_buffer is None:
            a.out_buffer = b.in_buffer = self.create_buffer()
        elif b.in_buffer is None:
            b.in_buffer = a.out_buffer
        else:
            a.out_buffer = b.in_buffer
