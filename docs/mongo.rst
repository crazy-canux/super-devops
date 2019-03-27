.. _mongo:

mongo
=====

`<https://github.com/andymccurdy/redis-py>`_

install
-------

install from pypi::

    $ pip install redis

usage
-----

import::

    import redis

functions::

    from_url(url, db=None, **kwargs)

Class Redis::

    Redis(host=u'localhost', port=6379, db=0, password=None,
    socket_timeout=None, socket_connect_timeout=None, socket_keepalive=None,
    socket_keepalive_options=None, connection_pool=None, unix_socket_path=None,
    encoding=u'utf-8', encoding_errors=u'strict', charset=None, errors=None,
    decode_responses=False, retry_on_timeout=False, ssl=False, ssl_keyfile=None,
    ssl_certfile=None, ssl_cert_reqs=u'required', ssl_ca_certs=None,
    max_connections=None)
    decode_responses: storage as string not byte.

    # methods
    pipeline(transcation=True, shard_hint=None) # transcation means all command atomically.

    >>> connection
    ping()
    echo(self, value)
    slaveof(self, host=None, port=None)

    >>> server
    save() # save data to disk, blocking untail save complete.
    dbsize()
    flushall(asynchronous=False) # delete all keys in all database on current host.
    flushdb(asynchronous=False) # delete all keys in the current database.

    >>> sentinel
    sentinel(self, *args)
    sentinel_get_master_addr_by_name(self, service_name)
    sentinel_master(self, service_name)
    sentinel_masters(self)
    sentinel_monitor(self, name, ip, port, quorum)
    sentinel_remove(self, name)
    sentinel_sentinels(self, service_name)
    sentinel_set(self, name, option, value)
    sentinel_slaves(self, service_name)

    >>> transaction
    exec()
    watch(*names)
    unwatch()

    >>> keys
    delete(*names) # delete one or more keys.
    dump(name)
    exists(*names)
    expire(self, name, time)
    expireat(name, when)
    keys(pattern=u'*') # return all keys matching pattern
    wait(...)
    scan(cursor=0, match=None, count=None) #

    >>> string
    append(key, value)
    get(name)
    getset(name, value)
    set(name, value, ex=None, px=None, nx=False, xx=False)
    strlen(...)
    mset(...)
    mget(...)

    >>> list
    blpop(keys, timeout=0)
    brpop(keys, timeout=0)
    brpoplpush(src, dst, timeout=0)
    lindex(name, index)
    linsert(name, where, refvalue, value)
    llen(name)
    lpop(name)
    lpush(name, *values)
    lset(name, index, value)
    rpop(name)
    rpush(name, *values)

    >>> hash
    hdel(name, *keys) # delete keys from hash.
    hexists(name, key)
    hget(name, key)
    hset(name, key, value)
    hgetall(name) # return python dict.
    hkeys(name)
    hlen(name)
    hmget(name, keys, *args) # return a list of values ordered by keys
    hmset(name, mapping)
    hscan(name, cursor=0, match=None, count=None)

    >>> set
    sadd(name, *values)
    sdiff(keys, *args)
    smove(src, dst, value)
    spop(name, count=None)
    srem(name, *values)
    sscan(name, cursor=0, match=None, count=None)

    >>> sorted set
    zadd(name, mapping, nx=False, xx=False, ch=False, incr=False)
    zrem(name, *values)
    zscan(name, cursor=0, match=None, count-None, score_cast_func<type'float'>)
    bzpopmax(keys, timeout=0)
    bzpopmin(keys, timeout=0)

    >>> streams

    >>> geo

Class Pipeline(Redis)::

    # method
    execute(raise_on_error=True)
    execute_command(*args, **kwargs)
    immediate_execute_command(*args, **options)

Class Sentinel::

    from redis.sentinel import Sentinel
    sentinel = Sentinel([('localhost', 26379)], socket_timeout=0.1)
    sentinel.discover_master('mymaster')
    sentinel.discover_slaves('mymaster')

    通过sentinel 操作master 或 slaves，master可以读写，slave只能读
    master = sentinel.master_for('mymaster', socket_timeout=0.1)
    slave = sentinel.slave_for('mymaster', socket_timeout=0.1)
    master.set('foo', 'bar')
    slave.get('foo')
