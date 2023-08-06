import json
from unittest import TestCase
from unittest import SkipTest

try:
    import MySQLdb
except Exception:
    raise SkipTest('Skipping due to version incompatibility')

from stackifyapm.base import Client
from stackifyapm.conf import constants
from stackifyapm.traces import execution_context
from stackifyapm.instrumentation import register
from stackifyapm.instrumentation import control


CONFIG = {
    "SERVICE_NAME": "service_name",
    "ENVIRONMENT": "production",
    "HOSTNAME": "sample_host",
    "FRAMEWORK_NAME": "framework",
    "FRAMEWORK_VERSION": "1.0",
    "APPLICATION_NAME": "sample_application",
    "BASE_DIR": "path/to/application/",
    "PREFIX_ENABLED": True,
}


class MySQLInstrumentationTest(TestCase):
    def setUp(self):
        self.client = Client(CONFIG)
        register._cls_registers = {
            "stackifyapm.instrumentation.packages.mysql.MySQLInstrumentation",
        }

        self.params = {
            'database': 'test',
            'password': 'password',
            'user': 'user',
            'host': '127.0.0.1',
            'port': 1112,
        }

        self.conn = MySQLdb.connect(**self.params)
        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE TABLE testdb(id INT, name VARCHAR(30));")
        self.conn.commit()

        control.instrument()
        self.client.begin_transaction("transaction_test")

    def tearDown(self):
        control.uninstrument()
        self.cursor.execute("DROP TABLE testdb;")
        self.conn.commit()

    def test_execute(self):
        self.conn = MySQLdb.connect(**self.params)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM testdb WHERE name LIKE 'JayR'")
        self.conn.commit()

        transaction = execution_context.get_transaction()
        assert transaction
        assert transaction.get_spans()

        span = transaction.get_spans()[0]
        span_data = span.to_dict()

        assert span_data['reqBegin']
        assert span_data['reqEnd']
        assert span_data['transaction_id']
        assert span_data['call'] == 'db.mysql.sql'
        assert span_data['props']
        assert span_data['props']['CATEGORY'] == 'Database'
        assert span_data['props']['SUBCATEGORY'] == 'Execute'
        assert span_data['props']['COMPONENT_CATEGORY'] == 'DB Query'
        assert span_data['props']['COMPONENT_DETAIL'] == 'Execute SQL Query'
        assert span_data['props']['PROVIDER'] == 'mysql'
        assert span_data['props']['SQL'] == 'SELECT * FROM testdb WHERE name LIKE \'JayR\''
        assert not span_data['props'].get('SQL_TRUNCATED')

    def test_truncated_statement(self):
        statement = "SELECT * FROM testdb WHERE name LIKE '{}'".format("X" * 100000)
        self.conn = MySQLdb.connect(**self.params)
        self.cursor = self.conn.cursor()
        self.cursor.execute(statement)
        self.conn.commit()

        transaction = execution_context.get_transaction()
        assert transaction
        assert transaction.get_spans()

        span = transaction.get_spans()[0]
        span_data = span.to_dict()

        assert span_data['reqBegin']
        assert span_data['reqEnd']
        assert span_data['transaction_id']
        assert span_data['call'] == 'db.mysql.sql'
        assert span_data['props']
        assert span_data['props']['CATEGORY'] == 'Database'
        assert span_data['props']['SUBCATEGORY'] == 'Execute'
        assert span_data['props']['COMPONENT_CATEGORY'] == 'DB Query'
        assert span_data['props']['COMPONENT_DETAIL'] == 'Execute SQL Query'
        assert span_data['props']['PROVIDER'] == 'mysql'
        assert len(span_data['props']['SQL']) == constants.SQL_STATEMENT_MAX_LENGTH
        assert span_data['props']['SQL_TRUNCATED']

    def test_prepared_statement(self):
        self.conn = MySQLdb.connect(**self.params)
        self.cursor = self.conn.cursor()

        query_statement = "SELECT * FROM testdb WHERE name LIKE %s"
        argument = ('JayR',)

        try:
            self.cursor.execute(query_statement, argument)
            self.conn.commit()
        except Exception:
            raise SkipTest('Skipping due to version incompatibility')

        transaction = execution_context.get_transaction()

        assert transaction
        assert transaction.get_spans()

        span = transaction.get_spans()[0]
        span_data = span.to_dict(config=self.client.config)

        assert span_data['reqBegin']
        assert span_data['reqEnd']
        assert span_data['transaction_id']
        assert span_data['call'] == 'db.mysql.sql'
        assert span_data['props']
        assert span_data['props']['CATEGORY'] == 'Database'
        assert span_data['props']['SUBCATEGORY'] == 'Execute'
        assert span_data['props']['COMPONENT_CATEGORY'] == 'DB Query'
        assert span_data['props']['COMPONENT_DETAIL'] == 'Execute SQL Query'
        assert span_data['props']['PROVIDER'] == 'mysql'
        assert span_data['props']['SQL'] == 'SELECT * FROM testdb WHERE name LIKE %s'
        assert span_data['props']['SQL_PARAMETERS'] == json.dumps([{1: 'JayR'}])

    def test_prepared_statement_with_multiple_params(self):
        self.conn = MySQLdb.connect(**self.params)
        self.cursor = self.conn.cursor()

        query_statement = "SELECT * FROM testdb WHERE name LIKE %s OR name LIKE %s"
        argument = ('JayR', 'Python')

        try:
            self.cursor.execute(query_statement, argument)
            self.conn.commit()
        except Exception:
            raise SkipTest('Skipping due to version incompatibility')

        transaction = execution_context.get_transaction()

        assert transaction
        assert transaction.get_spans()

        span = transaction.get_spans()[0]
        span_data = span.to_dict(config=self.client.config)

        assert span_data['reqBegin']
        assert span_data['reqEnd']
        assert span_data['transaction_id']
        assert span_data['call'] == 'db.mysql.sql'
        assert span_data['props']
        assert span_data['props']['CATEGORY'] == 'Database'
        assert span_data['props']['SUBCATEGORY'] == 'Execute'
        assert span_data['props']['COMPONENT_CATEGORY'] == 'DB Query'
        assert span_data['props']['COMPONENT_DETAIL'] == 'Execute SQL Query'
        assert span_data['props']['PROVIDER'] == 'mysql'
        assert span_data['props']['SQL'] == 'SELECT * FROM testdb WHERE name LIKE %s OR name LIKE %s'
        assert span_data['props']['SQL_PARAMETERS'] == json.dumps([{1: 'JayR'}, {2: 'Python'}])

    def test_prepared_statement_with_prefix_enabled_false(self):
        self.conn = MySQLdb.connect(**self.params)
        self.cursor = self.conn.cursor()

        query_statement = "SELECT * FROM testdb WHERE name LIKE %s"
        argument = ('JayR',)

        try:
            self.cursor.execute(query_statement, argument)
            self.conn.commit()
        except Exception:
            raise SkipTest('Skipping due to version incompatibility')

        transaction = execution_context.get_transaction()

        assert transaction
        assert transaction.get_spans()

        span = transaction.get_spans()[0]
        self.client.config.prefix_enabled = False
        span_data = span.to_dict(config=self.client.config)

        assert span_data['reqBegin']
        assert span_data['reqEnd']
        assert span_data['transaction_id']
        assert span_data['call'] == 'db.mysql.sql'
        assert span_data['props']
        assert span_data['props']['CATEGORY'] == 'Database'
        assert span_data['props']['SUBCATEGORY'] == 'Execute'
        assert span_data['props']['COMPONENT_CATEGORY'] == 'DB Query'
        assert span_data['props']['COMPONENT_DETAIL'] == 'Execute SQL Query'
        assert span_data['props']['PROVIDER'] == 'mysql'
        assert span_data['props']['SQL'] == 'SELECT * FROM testdb WHERE name LIKE %s'
        assert not span_data['props'].get('SQL_PARAMETERS')
