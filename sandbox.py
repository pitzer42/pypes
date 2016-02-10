from nodes import pipeline_node, PipelineNode
from process_pipeline_factory import ProcessPipelineFactory
from thread_pipeline_factory import ThreadPipelineFactory


@pipeline_node
def count():
    for i in range(50):
        yield i


@pipeline_node
def increment(i):
    return i + 1


increment2 = PipelineNode(increment)


@pipeline_node
def log(i):
    print(i)


count.connect(increment, increment2)
increment.connect(log)
increment2.connect(log)

t_pype = ThreadPipelineFactory()
t_pype.run_pipeline(count)

p_pype = ProcessPipelineFactory()
p_pype.run_pipeline(count)
