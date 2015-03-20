# coding:utf-8

import re
from datetime import datetime, date
from .exceptions import QueryFormatError

PLACEHOLDER = re.compile(r'.:+[0-9a-zA-Z_]+')


def qbind(fmt, **kwargs):
    def _(m):
        g = m.group(0)
        pre, key = g[0], g[1:]

        if pre == '\\':
            return key

        else:
            v = kwargs[key.lstrip(':')]
            should_escape = not key.startswith('::')
            return pre + qformat(v, should_escape)

    try:
        return PLACEHOLDER.sub(_, fmt)

    except KeyError as e:
        raise QueryFormatError(str(e))


def qformat(v, escape=True, nested=False):
    if isinstance(v, (int, long, float)):
        return str(v)

    elif isinstance(v, bool):
        return '1' if v else '0'

    elif isinstance(v, (str, unicode)):
        return "'{}'".format(str(v).replace("'", "\\'")) if escape else v

    elif v is None:
        return 'NULL'

    elif isinstance(v, (list, tuple, set)):
        s = ','.join([qformat(e, escape, True) for e in v])
        return '({})'.format(s) if nested else s

    elif isinstance(v, dict):
        d = {qformat(k, False, True): qformat(e, True, True)
             for k, e in v.items()}
        return ','.join(['{}={}'.format(k, e) for k, e in d.items()])

    elif isinstance(v, datetime):
        return "'{}'".format(v.strftime('%Y-%m-%d %H:%M:%S'))

    elif isinstance(v, date):
        dt = datetime(v.year, v.month, v.day)
        return "'{}'".format(dt.strftime('%Y-%m-%d'))

    elif hasattr(v, '__call__'):
        r = v()
        fname, args = (r[0], r[1:]) if isinstance(r, tuple) else (r, ())
        return '{}({})'.format(fname.upper(), qformat(args))

    raise TypeError('Incompatible type :{}'.format(v))
