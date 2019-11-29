from robot.utils import ConnectionCache


class Cache(ConnectionCache):

    """Customize connectioncache for super-devops."""

    _CONNECTIONS = {}
    _CLOSED = set()
    _CURRENT = None

    def __init__(self, alias_or_index=None):
        self._identifier = self._construct_unique_key(alias_or_index)

    def register(self, connection, alias_or_index=None):
        if not connection:
            raise ValueError('Invalid connection.')

        Cache._CURRENT = self._identifier if alias_or_index is None else \
            self._construct_unique_key(alias_or_index)
        Cache._CONNECTIONS[Cache._CURRENT] = connection
        return Cache._CURRENT

    @property
    def current(self):
        return Cache._CONNECTIONS.get(Cache._CURRENT)

    def _construct_unique_key(self, alias_or_index):
        alias_or_index = str(alias_or_index).strip() if alias_or_index else None
        if alias_or_index in Cache._CONNECTIONS:
            try:
                self._unregister(alias_or_index)
            except Exception:
                pass
        return alias_or_index or str(Cache._CONNECTIONS)

    def _unregister(self, alias_or_index):
        _connection = Cache._CONNECTIONS.get(alias_or_index)
        if _connection:
            try:
                _connection.quit()
                Cache._CLOSED.add(_connection)
            finally:
                if alias_or_index in Cache._CONNECTIONS:
                    Cache._CONNECTIONS[alias_or_index] = None
                    del Cache._CONNECTIONS[alias_or_index]

    def close(self, alias_or_index=None):
        alias_or_index = (
            str(alias_or_index).strip() if alias_or_index else None
        ) or (Cache._CURRENT)
        try:
            self._unregister(alias_or_index)
        except Exception as e:
            raise e
        finally:
            if Cache._CONNECTIONS:
                if alias_or_index == Cache._CURRENT:
                    Cache._CURRENT = Cache._CONNECTIONS.keys()[-1]
                else:
                    Cache._CURRENT = None

    def get_connection(self, alias_or_index=None):
        return Cache._CONNECTIONS.get(str(alias_or_index).strip() if alias_or_index else None)

    def switch(self, alias_or_index):
        alias_or_index = str(alias_or_index).strip() if alias_or_index else \
            None
        if alias_or_index in Cache._CONNECTIONS:
            Cache._CURRENT = alias_or_index
        return Cache._CONNECTIONS.get(Cache._CURRENT)

