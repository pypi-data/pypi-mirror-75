from functools import wraps

from time import time


def timeit(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        ts = time()
        result = f(*args, **kwargs)
        print("{} took {}".format(f.__name__, time() - ts))
        return result

    return wrap
