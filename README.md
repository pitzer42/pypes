# Pypes
Build a pipes and filters architecture using pure funcitons as filters:

```python
from pipeline import execute, pipeline_node


@pipeline_node
def count():
    for i in range(100):
        yield i


@pipeline_node
def increment(i):
    return i + 1


@pipeline_node
def double(i):
    return i * 2


@pipeline_node
def log(i):
    print(i)


count.connect(increment, double)
increment.connect(log)
double.connect(log)

execute(count)
```