# coding:utf-8


class Restructable(object):
    def mklist(self, key, separator=','):
        return self.process(_mklist(key, separator))

    def mkdict(self, **rules):
        return self.process(_mkdict(**rules))

    def mkdict_auto(self, **rules):
        return self.process(_mkdict_auto(**rules))

    def transpose(self, key, separator=','):
        return self.process(_transpose(key, separator))


class RestructableList(list, Restructable):
    def process(self, f):
        for e in self:
            f(e)
        return self


class RestructableDict(dict, Restructable):
    def process(self, f):
        f(self)
        return self


def _mklist(key, separator):
    def _(e):
        if e[key] is not None:
            e[key] = e[key].split(separator)

        else:
            e[key] = []

    return _


def _mkdict(**rules):
    def _(e):
        for fromkey, tokey in rules.items():
            keypath = tokey.split('.')
            head = e
            for k in keypath[:-1]:
                head = head.setdefault(k, RestructableDict())
            head[keypath[-1]] = e[fromkey]
            del e[fromkey]
    return _


def _mkdict_auto(**rules):
    def _(e):
        _rules = {}
        for k in e.keys():
            for from_prefix, tokey in rules.items():
                if k.startswith(from_prefix):
                    _k = k[len(from_prefix):]
                    _rules[k] = '{}.{}'.format(tokey, _k)
        f = _mkdict(**_rules)
        f(e)

    return _


def _transpose(key, separator):
    def _(e):
        ret = RestructableList()
        for k, joined in e[key].items():
            if joined is not None:
                splited = joined.split(separator)
                for i, v in enumerate(splited):
                    if len(ret) < i+1:
                        ret.append(RestructableDict())

                    ret[i][k] = v
        e[key] = ret

    return _
