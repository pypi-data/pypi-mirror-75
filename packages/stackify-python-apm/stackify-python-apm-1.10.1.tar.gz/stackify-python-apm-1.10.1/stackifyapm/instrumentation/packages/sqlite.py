from stackifyapm.exceptions import StackifyAPMException
from stackifyapm.instrumentation.decorators import call_exception_handler
from stackifyapm.instrumentation.packages.dbapi2 import (
    ConnectionProxy,
    CursorProxy,
    DbApi2Instrumentation,
)
from stackifyapm.traces import CaptureSpan
from stackifyapm.utils import get_method_name
from stackifyapm.utils.helper import is_async_span


class SQLiteCursorProxy(CursorProxy):
    provider_name = "sqlite"
    name = "GENERIC"


class SQLiteConnectionProxy(ConnectionProxy):
    cursor_proxy = SQLiteCursorProxy
    provider_name = "sqlite"
    name = "GENERIC"

    def _trace_sql(self, method, sql, params):
        kind = "db.sqlite.sql"
        context = {
            'CATEGORY': 'Database',
            'SUBCATEGORY': get_method_name(method).capitalize(),
            'COMPONENT_CATEGORY': 'DB Query',
            'COMPONENT_DETAIL': 'Execute SQL Query',
            'PROVIDER': self.name,
            'SQL': sql,
        }

        with CaptureSpan(kind, context, is_async=is_async_span()):
            if params is None:
                return method(sql)
            else:
                return method(sql, params)

    def execute(self, sql, params=None):
        return self._trace_sql(self.__wrapped__.execute, sql, params)

    def executemany(self, sql, params=None):
        return self._trace_sql(self.__wrapped__.executemany, sql, params)


class SQLiteInstrumentation(DbApi2Instrumentation):
    name = "GENERIC"

    instrument_list = [
        ("sqlite3", "connect"),
        ("sqlite3.dbapi2", "connect"),
        ("pysqlite2.dbapi2", "connect"),
    ]

    @call_exception_handler
    def call(self, module, method, wrapped, instance, args, kwargs):
        try:
            context = {
                'CATEGORY': 'Database',
                'SUBCATEGORY': 'Connect',
                'COMPONENT_CATEGORY': 'Database',
                'COMPONENT_DETAIL': 'Open Connection',
                'PROVIDER': self.name,
            }
        except Exception as e:
            raise StackifyAPMException(e)

        with CaptureSpan("db.sqlite.connect", context, is_async=is_async_span()):
            return SQLiteConnectionProxy(wrapped(*args, **kwargs))
