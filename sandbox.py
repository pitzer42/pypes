from Pipeline import Pipeline


def count():
    for i in range(1000):
        yield i


def increment(i):
    return i + 1


def combine(a, b):
    return (b, a),


def log(i):
    print(i)


p = Pipeline()
p.source(count)
p.par(combine, combine)
p.sink(log)
p.start()
