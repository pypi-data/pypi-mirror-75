class _A:
    def f(self):
        pass


FunctionType = type(_A.f)
MethodType = type(_A().f)
