# coding:utf-8

import pytest
import sqlite3
from sqlew import Client
from sqlew.exceptions import UnacceptableResultError

dbc = Client(sqlite3, database='tests/test_db.db')


def test_scalar():
    dbc.query_log = True
    assert dbc.exew('SELECT 1').scalar() == 1


def test_with():
    with dbc as d:
        assert d.exew('SELECT 1').scalar() == 1


def test_insert():
    dbc.exes('DROP TABLE IF EXISTS test_insert').commit()
    dbc.exes("""CREATE TABLE test_insert (
             id integer primary key,
             name text)""")
    i = (dbc.exes('INSERT INTO test_insert VALUES (null, "name")')
            .commit().lastid())
    assert i == 1
    dbc.exew('SELECT * FROM test_insert').first() == (1, 'name')

    pytest.raises(UnacceptableResultError,
                  dbc.exew('SELECT * FROM test_insert WHERE id = 100').first,
                  False)


def test_update():
    dbc.exes('DROP TABLE IF EXISTS test_update').commit()
    dbc.exes("""CREATE TABLE test_update (
             id integer primary key,
             name text)""")
    dbc.exes('INSERT INTO test_update VALUES (null,"name")').commit().lastid()

    i = dbc.exes('UPDATE test_update SET name = "name2"').commit().rowcount()
    assert i == 1
