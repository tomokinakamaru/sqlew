# coding:utf-8

from . import compat


class RestructableDict(dict):
    def nest(self, *keypath):
        rst, name = self._find_target(*keypath)
        keys = list(rst.keys())
        d = {k[len(name)+1:]: rst.pop(k) for k in keys
             if k.startswith(name + '_')}
        rst[name] = RestructableDict(d)
        return self

    def split(self, *keypath):
        rst, name = self._find_target(*keypath)
        rst[name] = RestructableList(rst[name].split(','))
        return self

    def invert(self, *keypath):
        rst, name = self._find_target(*keypath)
        keys = rst[name].keys()
        ls = [dict(zip(keys, e))
              for e in compat.zip_longest(*rst[name].values())]
        rst[name] = RestructableList(ls)
        return self

    def nest_list(self, *keypath):
        self.nest(*keypath)
        rst, name = self._find_target(*keypath)
        for k in rst[name].keys():
            rst[name].split(k)
        return self.invert(*keypath)

    def _find_target(self, *keypath):
        return compat.keypath_value(self, *keypath), keypath[-1]


class RestructableList(list):
    def nest(self, *keypath):
        for e in self:
            e.nest(*keypath)
        return self

    def split(self, *keypath):
        for e in self:
            e.split(*keypath)
        return self

    def invert(self, *keypath):
        for e in self:
            e.invert(*keypath)
        return self

    def nest_list(self, *keypath):
        for e in self:
            e.nest_list(*keypath)
        return self
