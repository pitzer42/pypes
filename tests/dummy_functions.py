from nodes import pipeline_node


@pipeline_node
def count():
    for i in range(count.until):
        yield i
count.until = 10


@pipeline_node
def increment(i):
    return i + 1


def log(i):
    print(i)


def save_to(queue):
    @pipeline_node
    def save_to_queue(i):
        queue.put(i)

    return save_to_queue
