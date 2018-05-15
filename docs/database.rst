.. _database:

SQLAlchemy
==========

ORM.

install
-------

install from pypi::

    $ pip install sqlalchemy

usage
-----

import::

    from sqlalchemy import create_engine
    from sqlalchemy import exc

class Engine::

    Engine(pool, dialect, url, logging_name=None, echo=None, proxy=None, execution_options=None)
    # methods:
    begin(self, close_with_result=False) # return Connection object
    with engine.begin() as conn:
        conn.execute("insert into table (x, y, z) values (1, 2, 3)")
    connect(self, **kwargs) # return Connection object
    execution_options(self, **opt)
    execute(self, statement, *multiparams, **params)

class Connection::

    Connection(engine, connection=None, close_with_result=False, _branch_from=None, _execution_options=None, _dispatch=None, _has_events=None)
    # methods:
    begin(self) # Return Transaction object.
    close(self)
    scalar(self, object, *multiparams, **params)
    execute(self, object, *multiparams, **params) # return ResultProxy object.
    execution_options(self, **opt) # return a copy of Connection object.
    ## opt
    autocommit:
    compiled_cache:
    isolation_level:
    no_parameters:
    stream_results:
    schema_translate_map:
    result_proxy = connection.execution_options(stream_results=True).execute(stmt)

class Transaction::

    Transaction(connection, parent)
    # methods:
    close()
    rollback()
    commit()

class ResultProxy::

    ResultProxy(context)
    # methods:
    keys()    # [key0, key1, ...]
    scalar(self)
    process_rows(self, rows)
    first(self)
    fetchone(self)
    fetchmany(self, size=None)
    fetchall(self) # [RowProxy0, RowProxy1, ...]
    close(self)
    rowcount
    inserted_primary_key
    # data
    lastrowid

class RowProxy::

    RowProxy(BaseRowProxy)
    # methods:
    has_key(key)
    items()
    keys()
    iterkeys()
    itervalues()

functions::

    create_engine(*args, **kwargs) # return Engine object.
    # dialect[+driver]://user:password@host/dbname[?key=value..]
    engine = create_engine("postgresql+psycopg2://scott:tiger@hostname:port/test")
    engine = create_engine("mysql+pymysql://scott:tiger@hostname:port/dbname")
    enigne = create_engine("oracle+cx_oracle://scott:tiger@hostname:port/dbname')
    engine = create_engine("mssql+pymssql://scott:tiger@hostname:port/dbname/?charset=utf8")
    ## args/kwargs:
    connect_args
    creator
    case_sensitive=True
    convert_unicode=False
    echo=False
    echo_pool=False
    encoding=utf-8
    execution_options
    implicit_returning=True
    isolation_level
    label_length=None
    listeners
    logging_name
    max_overflow=10
    module=None
    paramstyle=None
    pool=None
    poolclass=None
    pool_logging_name
    pool_size=5
    pool_timeout=30
    pool_recycle=-1
    pool_reset_on_return='rollback'
    strategy='plain'
    executor=None
