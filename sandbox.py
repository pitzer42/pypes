from pipeline import execute_threads, execute_processes, pipeline_node, PipelineNode


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

execute_threads(count)
execute_processes(count)
