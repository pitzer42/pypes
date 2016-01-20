import unittest
from Pipeline import Pipeline


def count(n):
    def inner():
        for i in range(n):
            yield i
    return inner()


def increment(i):
    return i + 1


def log(i):
    print(i)


class TestPipeline(unittest.TestCase):
    def test_pipeline_has_sources(self):
        p = Pipeline()
        p.src(count(10))
        p.seq(increment)
        p.snk(log)
        p.start()


if __name__ == '__main__':
    unittest.main()
