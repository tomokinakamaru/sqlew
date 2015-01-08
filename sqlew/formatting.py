# coding:utf-8

import re
from datetime import datetime

PLACEHOLDER = re.compile(r'{(.*?)}')
RAW_PLACEHOLDER = re.compile(r'{{(.*?)}}')


def qformat(fmt, **kwargs):
    ph = lambda m: escape(kwargs[m.group(1)])
    rph = lambda m: str(kwargs[m.group(1)])
    return PLACEHOLDER.sub(ph, RAW_PLACEHOLDER.sub(rph, fmt))


def escape(v):
    if isinstance(v, (int, long, float)):
        return str(v)

    elif isinstance(v, bool):
        return '1' if v else '0'

    elif isinstance(v, (str, unicode)):
        return "'{}'".format(str(v).replace("'", "\\'"))

    elif v is None:
        return 'NULL'

    elif isinstance(v, (list, tuple, set)):
        return ','.join([value(e) for e in v])

    elif isinstance(v, datetime):
        return "'{}'".format(v.strftime('%Y-%m-%d %H:%M:%S'))

    raise TypeError('Incompatible type :{}'.format(v))
