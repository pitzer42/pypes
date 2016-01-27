# Pypes
Build a pipes and filters architecture using pure funcitons as filters:

### Example
```python
from pipeline import execute, pipeline_node, PipelineNode


@pipeline_node
def count():
    for i in range(100):
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

execute(count)
```

### TODO
  - Remove duplication on modules process_pipeline and thread_pipeline. Probably using strategy pattern.
  - Test the use of processes and threads in the same pipeline
  - Build example application
