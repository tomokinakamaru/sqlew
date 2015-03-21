# coding:utf-8

import pytest
import sqlite3
from sqlew import Client


dbc = Client(sqlite3, database='tests/test_db.db')


def clear_table():
    dbc.exew('DROP TABLE IF EXISTS test')
    dbc.exew('CREATE TABLE test (id integer primary key, name test)')


def test_split():
    clear_table()
    dbc.exes("INSERT INTO test (name) VALUES (NULL)").commit()
    r = dbc.exew('SELECT * FROM test LIMIT 1').all()
    assert r.split('name') == [{'id': 1, 'name': []}]

    clear_table()
    dbc.exes("INSERT INTO test (name) VALUES ('aaa,bbb,ccc')").commit()
    r = dbc.exew('SELECT * FROM test LIMIT 1').all()
    assert r.split('name') == [{'id': 1, 'name': ['aaa', 'bbb', 'ccc']}]


def test_form():
    clear_table()
    dbc.exes("INSERT INTO test (name) VALUES ('xxx')").commit()

    r = dbc.exew('SELECT id, name as x_name FROM test').all()
    assert r.form('x_', 'x') == [{'id': 1, 'x': {'name': 'xxx'}}]

    r = dbc.exew('SELECT id, name FROM test').all()
    assert r.form_one('name', 'x.name') == [{'id': 1, 'x': {'name': 'xxx'}}]
    r = dbc.exew('SELECT id, name FROM test').all()
    print r.form_one('name', 'x.name')
    print r.form_one('x.name', 'name')
    assert r == [{'id': 1, 'name': 'xxx', 'x': {}}]


def test_transpose():
    clear_table()
    dbc.exes("INSERT INTO test (name) VALUES ('aaa,bbb')").commit()

    r = dbc.exew("""SELECT id, name AS x_name, '123,456' as x_id
                    FROM test""").all()
    r.form('x_', 'x').transpose('x')
    assert r == [{'id': 1,
                  'x': [{'name': 'aaa', 'id': '123'},
                        {'name': 'bbb', 'id': '456'}]}]
