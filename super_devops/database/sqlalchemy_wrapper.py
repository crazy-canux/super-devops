import logging

from sqlalchemy import create_engine
from sqlalchemy import exc


logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy').setLevel(logging.WARNING)


class BaseDB(object):

    def __init__(
            self, dialect=None, host=None, username=None, password=None,
            database=None, driver=None, port=None, **kwargs
    ):
        """Init db engine.

        connect_args
        creator
        execution_options
        isolation_level
        listeners
        logging_name
        pool_logging_name

        case_sensitive=True
        convert_unicode=False
        echo=False
        echo_pool=False
        encoding=utf-8
        implicit_returning=True
        label_length=None
        max_overflow=10
        module=None
        paramstyle=None
        pool=None
        poolclass=None
        pool_size=5
        pool_timeout=30
        pool_recycle=-1
        pool_reset_on_return='rollback'
        strategy='plain'
        executor=None
        """
        self.dialect = dialect if dialect else (
            self.__get_dialect_from_port(port) or \
            self.__get_dialect_from_driver(driver)
        )
        self.driver = driver if driver else (
            self.__get_driver_from_dialect(dialect) or \
            self.__get_driver_from_port(port)
        )
        self.port = port if port else (
            self.__get_port_from_dialect(dialect) or \
            self.__get_port_from_driver(driver)
        )
        self.host = host
        self.username = username
        self.password = password
        self.database = database

        self.case_sensitive = kwargs.get('case_sensitive', True)
        self.convert_unicode = kwargs.get('convert_unicode', False)
        self.echo = kwargs.get('echo', False)
        self.echo_pool = kwargs.get('echo_pool', False)
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.implicit_returning = kwargs.get('implicit_returning', True)
        self.label_length = kwargs.get('label_length', None)
        self.max_overflow = kwargs.get('max_overflow', 10)
        self.module = kwargs.get('module', None)
        self.paramstyle = kwargs.get('paramstype', None)
        self.pool = kwargs.get('pool', None)
        self.poolclass = kwargs.get('poolclass', None)
        self.pool_size = kwargs.get('pool_size', 5)
        self.pool_timeout = kwargs.get('pool_timeout', 30)
        self.pool_recycle = kwargs.get('pool_recycle', -1)
        self.pool_reset_on_return = kwargs.get('pool_reset_on_return',
                                               'rollback')
        self.strategy = kwargs.get('strategy', 'plain')

        self.engine = None
        self.connection = None

    def __enter__(self):
        url = '{dialect}+{driver}://{username}:{password}@{host}:{port}/' \
              '{database}?charset=utf8'.format(
            dialect=self.dialect,
            driver=self.driver,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )
        self.engine = create_engine(
            url,
            case_sensitive=self.case_sensitive,
            convert_unicode=self.convert_unicode,
            echo=self.echo,
            echo_pool=self.echo_pool,
            encoding=self.encoding,
            implicit_returning=self.implicit_returning,
            label_length=self.label_length,
            max_overflow=self.max_overflow,
            module=self.module,
            paramstyle=self.paramstyle,
            pool=self.pool,
            poolclass=self.poolclass,
            pool_size=self.pool_size,
            pool_timeout=self.pool_timeout,
            pool_recycle=self.pool_recycle,
            pool_reset_on_return=self.pool_reset_on_return,
            strategy=self.strategy
        )
        self.connection = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def __get_dialect_from_driver(self, driver):
        dialect = None
        if driver in ['pymssql']:
            dialect = 'mssql'
        elif driver in ['pymysql']:
            dialect = 'mysql'
        elif driver in ['psycopg2']:
            dialect = 'postgresql'
        elif driver in ['cx_oracle']:
            dialect = 'oracle'
        return dialect

    def __get_dialect_from_port(self, port):
        dialect = None
        if port == 1433:
            dialect = 'mssql'
        elif port == 3306:
            dialect = 'mysql'
        elif port == 5432:
            dialect = 'postgresql'
        elif port == 1521:
            dialect = 'oracle'
        return dialect

    def __get_port_from_dialect(self, dialect):
        port = None
        if dialect == 'mssql':
            port = 1433
        elif dialect == 'mysql':
            port = 3306
        elif dialect == 'postgresql':
            port = 5432
        elif dialect == 'oracle':
            port = 1521
        return port

    def __get_port_from_driver(self, driver):
        port = None
        if driver in ['pymssql']:
            port = 1433
        elif driver in ['pymysql']:
            port = 3306
        elif driver in ['psycopg2']:
            port = 5432
        elif driver in ['cx_oracle']:
            port = 1521
        return port

    def __get_driver_from_dialect(self, dialect):
        driver = None
        if dialect == 'mssql':
            driver = 'pymssql'
        elif dialect == 'mysql':
            driver = 'pymysql'
        elif dialect == 'postgresql':
            driver = 'psycopg2'
        elif dialect == 'oracle':
            driver = 'cx_oracle'
        return driver

    def __get_driver_from_port(self, port):
        driver = None
        if port == 1433:
            driver = 'pymssql'
        elif port == 3306:
            driver = 'pymysql'
        elif port == 5432:
            driver = 'psycopg2'
        elif port == 1521:
            driver = 'cx_oracle'
        return driver

    def __execute(self, sql, autocommit=False):
        try:
            result = self.connection.execution_options(
                autocommit=autocommit
            ).execute(sql)
        except exc.DisconnectionError as e:
            raise Exception('Database Disconnected: ' + e.message)
        except exc.ProgrammingError as e:
            raise Exception('Execute sql failed: ' + e.message)
        except exc.DBAPIError as e:
            if e.connection_invalidated:
                raise Exception('Connection invalidated: ' + e.message)
        except Exception as e:
            raise e
        else:
            return result

    def execute_transaction(self, sql):
        try:
            with self.connection.begin():
                self.connection.execute(sql)
        except Exception:
            return False
        else:
            return True

    def delete_query(self, sql, ignore_error=False, autocommit=True):
        try:
            result_proxy = self.__execute(sql, autocommit)
            if result_proxy:
                return result_proxy.rowcount
        except exc.IntegrityError as e:
            if ignore_error:
                return None
            else:
                raise e
        except Exception as e:
            raise e

    def select_query(self, sql, autocommit=False):
        """return [(column1, ....), (column1, ...), ...]"""
        result_proxy = self.__execute(sql, autocommit)
        if result_proxy is None:
            return None
        else:
            results = result_proxy.fetchall()
        return results

