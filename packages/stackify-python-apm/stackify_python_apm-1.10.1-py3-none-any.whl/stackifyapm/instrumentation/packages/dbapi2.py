import json

from stackifyapm.exceptions import StackifyAPMException
from stackifyapm.instrumentation.decorators import call_exception_handler
from stackifyapm.instrumentation.packages.base import AbstractInstrumentedModule
from stackifyapm.traces import CaptureSpan
from stackifyapm.utils import wrapt, get_method_name
from stackifyapm.utils.helper import is_async_span


class CursorProxy(wrapt.ObjectProxy):
    provider_name = None
    name = None

    def callproc(self, procname, params=None):
        return self._trace_sql(self.__wrapped__.callproc, procname, params)

    def execute(self, sql, params=None):
        return self._trace_sql(self.__wrapped__.execute, sql, params)

    def executemany(self, sql, param_list):
        return self._trace_sql(self.__wrapped__.executemany, sql, param_list)

    def _bake_sql(self, sql):
        return sql

    def _trace_sql(self, method, sql, params):
        try:
            sql_string = self._bake_sql(sql)
            kind = "db.{0}.sql".format(self.provider_name)
            context = {
                'CATEGORY': 'Database',
                'SUBCATEGORY': get_method_name(method).capitalize(),
                'COMPONENT_CATEGORY': 'DB Query',
                'COMPONENT_DETAIL': 'Execute SQL Query',
                'PROVIDER': self.name or self.provider_name,
                'SQL': sql_string,
            }
            if params:
                sql_params = [{index: value} for index, value in enumerate(params, start=1)]
                context['SQL_PARAMETERS'] = json.dumps(sql_params)
        except Exception as e:
            raise StackifyAPMException(e)

        with CaptureSpan(kind, context, is_async=is_async_span()):
            if params is None:
                return method(sql)
            else:
                return method(sql, params)


class ConnectionProxy(wrapt.ObjectProxy):
    cursor_proxy = CursorProxy

    def cursor(self, *args, **kwargs):
        return self.cursor_proxy(self.__wrapped__.cursor(*args, **kwargs))


class DbApi2Instrumentation(AbstractInstrumentedModule):
    connect_method = None

    @call_exception_handler
    def call(self, module, method, wrapped, instance, args, kwargs):
        return ConnectionProxy(wrapped(*args, **kwargs))

    def call_if_sampling(self, module, method, wrapped, instance, args, kwargs):
        return self.call(module, method, wrapped, instance, args, kwargs)
