# coding:utf-8

import pytest
import sqlite3
from sqlew.restructables import (RestructableDict as RD,
                                 RestructableList as RL)


def test_nest_dict():
    rl = RL([RD({'a': 1, 'b': 100, 'c_x': 10, 'c_y': 20})])
    assert rl.nest('c') == [{'a': 1, 'b': 100, 'c': {'x': 10, 'y': 20}}]

    rl = RL([RD({'a': 1, 'b': 100})])
    assert rl.nest_dict('x', {'a': '-', 'b': '+'}) == [{'x': {'-': 1,
                                                              '+': 100}}]


def test_nest_list():
    rl = RL([RD({'a_x': '1,2', 'a_y': '4,5'})])
    assert rl.nest('a', ',') == [{'a': [{'x': '1', 'y': '4'},
                                        {'x': '2', 'y': '5'}]}]


def test_a():
    rl = RL([RD({'x': '1,2'})])
    print('-- rl --', rl)
    assert rl.nest_list('a', {'x': '*'}) == [{'a': [{'*': '1'}, {'*': '2'}]}]
