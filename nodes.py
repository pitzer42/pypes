def pipeline_node(func):
    """
    Decorates functions that can be connected with others to build a pipeline.
    """
    return PipelineNode(func)


class PipelineNode:
    """
    Function that can be connected with others to build a pipeline.
    """

    def __init__(self, func):
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
        self._func = func
        self.neighbors = []

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def connect(self, *args):
        self.neighbors += args

    def has_neighbors(self):
        return len(self.neighbors) > 0