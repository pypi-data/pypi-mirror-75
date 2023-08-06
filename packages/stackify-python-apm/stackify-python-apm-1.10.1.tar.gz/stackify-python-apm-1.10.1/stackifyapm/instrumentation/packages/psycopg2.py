from stackifyapm.exceptions import StackifyAPMException
from stackifyapm.instrumentation.decorators import call_exception_handler
from stackifyapm.instrumentation.packages.dbapi2 import (
    ConnectionProxy,
    CursorProxy,
    DbApi2Instrumentation,
)
from stackifyapm.traces import CaptureSpan
from stackifyapm.utils.helper import is_async_span


class PGCursorProxy(CursorProxy):
    provider_name = "postgresql"

    def _bake_sql(self, sql):
        if hasattr(sql, "as_string"):
            return sql.as_string(self.__wrapped__)
        return sql


class PGConnectionProxy(ConnectionProxy):
    cursor_proxy = PGCursorProxy


class Psycopg2Instrumentation(DbApi2Instrumentation):
    name = "psycopg2"

    instrument_list = [("psycopg2", "connect")]

    @call_exception_handler
    def call(self, module, method, wrapped, instance, args, kwargs):
        try:
            context = {
                "CATEGORY": "Database",
                "SUBCATEGORY": "Connect",
                "COMPONENT_CATEGORY": "Database",
                "COMPONENT_DETAIL": "Open Connection",
                "PROVIDER": self.name,
            }
        except Exception as e:
            raise StackifyAPMException(e)

        with CaptureSpan("db.postgresql.connect", context, is_async=is_async_span()):
            return PGConnectionProxy(wrapped(*args, **kwargs))


class Psycopg2RegisterTypeInstrumentation(DbApi2Instrumentation):
    name = "psycopg2-register-type"

    instrument_list = [
        ("psycopg2.extensions", "register_type"),
        ("psycopg2._json", "register_json"),
    ]

    @call_exception_handler
    def call(self, module, method, wrapped, instance, args, kwargs):
        try:
            if "conn_or_curs" in kwargs and hasattr(kwargs["conn_or_curs"], "__wrapped__"):
                kwargs["conn_or_curs"] = kwargs["conn_or_curs"].__wrapped__
            elif len(args) == 2 and hasattr(args[1], "__wrapped__"):
                args = (args[0], args[1].__wrapped__)
            elif method == "register_json":
                if args and hasattr(args[0], "__wrapped__"):
                    args = (args[0].__wrapped__,) + args[1:]
        except Exception as e:
            raise StackifyAPMException(e)

        return wrapped(*args, **kwargs)
