# coding:utf-8

from .formatting import qformat
from .restructables import RestructableList as RL, RestructableDict as RD


class Client(object):
    def __init__(self, dbapi, **kwargs):
        self.nocommit = False

        self._dbapi = dbapi
        self._config = kwargs

        self._autoclose = True

        self._connection = None
        self._cursor = None

        self._result_cols = None
        self._result_rows = None
        self._lastrowid = None
        self._rowcount = None

    @property
    def noclose(self):
        self._autoclose = False
        return self

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self._dbapi.connect(**self._config)
        return self._connection

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self.connection.cursor()
        return self._cursor

    @property
    def scalar(self):
        if len(self._result_rows) > 0:
            return self._result_rows[0][0]

        else:
            return None

    @property
    def lastid(self):
        return self._lastrowid

    @property
    def rowcount(self):
        return self._rowcount

    @property
    def first(self):
        if len(self._result_rows) > 0:
            return RD(dict(zip(self._result_cols, self._result_rows[0])))

        else:
            return None

    @property
    def all(self):
        return RL([dict(zip(self._result_cols, r)) for r in self._result_rows])

    def commit(self):
        if not self.nocommit:
            self.connection.commit()
        return self

    def rollback(self):
        self.connection.rollback()
        return self

    def close(self):
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None

        if self._connection is not None:
            self._connection.close()
            self._connection = None

        return self

    def exe(self, fmt, **kwargs):
        self.cursor.execute(qformat(fmt, **kwargs))
        self._result_cols = [c[0] for c in self.cursor.description]
        self._result_rows = [r for r in self.cursor]
        self._lastrowid = self.cursor.lastrowid
        self._rowcount = self.cursor.rowcount

        if self._autoclose:
            self.close()

        else:
            self._autoclose = True

        return self
