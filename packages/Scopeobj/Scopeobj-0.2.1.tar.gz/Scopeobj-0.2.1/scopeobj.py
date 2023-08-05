from builtins import exec as _builtin_exec, eval as _builtin_eval

class Scope(object):
    
    def __init__(self, settings={}):
        if not isinstance(settings, dict): raise TypeError("Arg 'settings' must be a dict object")
        self.settings = settings
        if not settings:
            self.exec('from builtins import *')
    
    def getitem(self, key, none_default=None):
        return self.settings.get(key, none_default)
    
    def setitems(self, settings):
        self.settings.update(settings)
    
    def getitems(self, *keys, none_default):
        result = []
        for key in keys:
            result.append(self.getitem(key, none_default))
        return result
    
    def setitem(self, key, value):
        self.setitems({key: value})
    
    def exec(self, s):
        _builtin_exec(s, self.settings)
    
    def eval(self, s):
        return _builtin_eval(s, self.settings)
    
    def keys(self):
        return list(self.settings.keys())
    
    def clear(self):
        self.settings.clear()
    
    def __add__(self, scope):
        keys = list(set(scope.keys()+self.keys()))
        result = {}
        for i in range(len(keys)):
            result[keys[i]] = self.getitem(keys[i], scope.getitem(keys[i]))
        s = Scope()
        s.clear()
        s.setitems(result)
        return s
    
    def __sub__(self, scope):
        keys = list(set(scope.keys())-set(self.keys()))
        result = {}
        for i in range(len(keys)):
            result[keys[i]] = self.getitem(keys[i], scope.getitem(keys[i]))
        s = Scope()
        s.clear()
        s.setitems(result)
        return s
    
    def __radd__(self, scope):
        return scope+self
    
    def __rsub__(self, scope):
        return scope-self
    
    def __bool__(self):
        return bool(self.settings)
    
    def __dict__(self):
        return self.settings
    
    def __list__(self):
        return(self.settings.keys)

    def __tuple__(self):
        return tuple(list(self))
    
    def __repr__(self):
        return '<Scope object at module scopeobj>'
    
    def __len__(self):
        return len(list(self))