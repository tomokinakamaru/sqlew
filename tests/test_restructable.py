# coding:utf-8

import pytest
import sqlite3
from sqlew.restructables import (RestructableDict as RD,
                                 RestructableList as RL)


def test_nest():
    rl = RL([RD({'a': 1, 'b': 100, 'c_x': 10, 'c_y': 20})])
    assert rl.nest('c') == [{'a': 1, 'b': 100, 'c': {'x': 10, 'y': 20}}]


def test_split():
    rl = RL([RD({'a': {'b': '1,2,3'}})])
    assert rl.split('a', 'b') == [{'a': {'b': ['1', '2', '3']}}]


def test_invert():
    rl = RL([RD({'a': {'x': [1, 2], 'y': [3, 4]}})])
    assert rl.invert('a') == [{'a': [{'x': 1, 'y': 3},
                                     {'x': 2, 'y': 4}]}]


def test_nest_list():
    rl = RL([RD({'a_x': '1,2', 'a_y': '4,5'})])
    assert rl.nest_list('a') == [{'a': [{'x': '1', 'y': '4'},
                                        {'x': '2', 'y': '5'}]}]
