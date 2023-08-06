class cached_property:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        func_name = self.func.__name__
        result = instance.__dict__[func_name] = self.func(instance)
        return result
