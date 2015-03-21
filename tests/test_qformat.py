# coding:utf-8

import pytest
from datetime import datetime, date
from sqlew import queryformat
from sqlew.exceptions import (QueryFormatError,
                              IncompatibleTypeError)


@pytest.mark.parametrize('fmt, ret',
                         [(':x', "'a'"),
                          (' :x', " 'a'"),
                          ('_:x', "_'a'"),
                          ('::x', "a"),
                          ('\::x', '::x')])
def test_placeholoder(fmt, ret):
    assert queryformat.qformat(fmt, x='a') == ret


def test_placeholder_error():
    pytest.raises(QueryFormatError, queryformat.qformat, ':x', y=1)


@pytest.mark.parametrize('n',
                         [1, -1,
                          1.0, -1.23,
                          10000000000000000000000000000000000])
def test_numbers(n):
    assert queryformat.qformat(':n', n=n) == str(n)


@pytest.mark.parametrize('s, ret',
                         [('string', "'string'"),
                          (u'unicode', u"'unicode'"),
                          (u'ああああ', u"'ああああ'")])
def test_str(s, ret):
    assert queryformat.qformat(':s', s=s) == ret


@pytest.mark.parametrize('b, ret', [(True, '1'), (False, '0')])
def test_bool(b, ret):
    assert queryformat.qformat(':b', b=b) == ret


def test_none():
    assert queryformat.qformat(':n', n=None) == 'NULL'


@pytest.mark.parametrize('ls, ret',
                         [([1, 2], '1,2'),
                          ([1, [1, 2]], '1,(1,2)'),
                          ([1, [1, [1, 2]]], '1,(1,(1,2))')])
def test_list(ls, ret):
    assert queryformat.qformat(':ls', ls=ls) == ret


@pytest.mark.parametrize('d, ret',
                         [({'a': 1, 'b': True, 'c': [1, 2]},
                           'a=1,c=(1,2),b=1')])
def test_dict(d, ret):
    for e in queryformat.qformat(':d', d=d).split(','):
        assert e in ret.split(',')


@pytest.mark.parametrize('f, ret',
                         [(lambda: 'now', 'NOW()'),
                          (lambda: ('sha2', 'a', 256), "SHA2('a',256)")])
def test_func(f, ret):
    assert queryformat.qformat(':f', f=f) == ret


def test_datetime():
    dt = datetime.utcnow()
    ret = dt.strftime("'%Y-%m-%d %H:%M:%S'")
    assert queryformat.qformat(':dt', dt=dt) == ret


def test_date():
    dt = date.today()
    ret = datetime(dt.year, dt.month, dt.day).strftime("'%Y-%m-%d'")
    assert queryformat.qformat(':dt', dt=dt) == ret


def test_incompat():
    pytest.raises(IncompatibleTypeError,
                  queryformat.qformat, ':o', o=object())
