Scopeobj is a Python module. You can use it as a scope.
For example:
>>> from scopeobj import Scope
>>> s = Scope()
>>> s.exec("x = 3")
>>> s.eval("x ** 2")
9
>>> s.clear()
>>> s.getitem("x")
None