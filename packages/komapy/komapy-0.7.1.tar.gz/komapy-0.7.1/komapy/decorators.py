from functools import partial


class counter:
    """
    A counter decorator to track how many times a function is called.
    """

    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)


def register_as_decorator(func):
    """
    Register extensions, transforms, or addons function as decorator.
    """
    def wrapper(*args, **kwargs):
        # If argument length < 2, user just provides function name without its
        # resolver. So return partial function. Otherwise, return original
        # function.
        if len(args) < 2:
            return partial(func, *args, **kwargs)
        return partial(func, *args, **kwargs)()
    return wrapper
