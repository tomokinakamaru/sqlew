# coding:utf-8

import pytest
import sqlite3
from sqlew import Client
from sqlew.exceptions import UnacceptableResultError

dbc = Client(sqlite3, database='tests/test_db.db')


def clear_table():
    dbc.exew('DROP TABLE IF EXISTS test')
    dbc.exew('CREATE TABLE test (id integer primary key, name test)')


def test_with():
    with dbc as d:
        d.exew('SELECT 1')


def test_rollback():
    clear_table()

    q = "INSERT INTO test (name) VALUES ('aaa bbb')"
    dbc.exew(q).commit()
    assert dbc.exew('SELECT COUNT(*) FROM test').scalar() == 0

    dbc.rollback()
    assert dbc.exew('SELECT COUNT(*) FROM test').scalar() == 0


def test_badqsql():
    dbc.query_log = True
    pytest.raises(sqlite3.OperationalError, dbc.exew, 'SELECT 1, 2, 3 FROM')


def test_insert():
    clear_table()

    q = "INSERT INTO test (name) VALUES ('aaa bbb')"
    dbc.exew(q).commit()
    assert dbc.exew('SELECT COUNT(*) FROM test').scalar() == 0

    dbc.exes(q).commit()
    assert dbc.exew('SELECT COUNT(*) FROM test').scalar() == 1


def test_scalar():
    clear_table()
    pytest.raises(UnacceptableResultError,
                  dbc.exew('SELECT 1 FROM test').scalar,
                  False)


def test_lastid():
    clear_table()
    q = "INSERT INTO test (name) VALUES ('aaa bbb')"
    assert dbc.exes(q).commit().lastid() == 1

    q = "SELECT * FROM test"
    pytest.raises(UnacceptableResultError,
                  dbc.exew(q).commit().lastid,
                  False)


def test_rowcount():
    clear_table()
    q = "INSERT INTO test (name) VALUES ('aaa bbb')"
    dbc.exes(q).commit()

    q = "UPDATE test SET name = 'aaa bbb'"
    assert dbc.exes(q).commit().rowcount() == 1

    q = "UPDATE test SET name = 'aaa bbb' WHERE id = 100"
    assert dbc.exes(q).commit().rowcount() == 0
    pytest.raises(UnacceptableResultError,
                  dbc.exes(q).commit().rowcount,
                  False)


def test_first():
    clear_table()
    assert dbc.exew('SELECT * FROM test').first() is None

    q = "INSERT INTO test (name) VALUES ('aaa bbb')"
    dbc.exes(q).commit()
    assert dbc.exew('SELECT id FROM test').first() == {'id': 1}


def test_all():
    clear_table()
    pytest.raises(UnacceptableResultError,
                  dbc.exew('SELECT * FROM test').all,
                  False)

    q = "INSERT INTO test (name) VALUES ('aaa bbb')"
    dbc.exes(q).commit()
    assert dbc.exew('SELECT id FROM test').all() == [{'id': 1}]
