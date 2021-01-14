import logging

import ldap3
from ldap3 import Server, Connection, Tls

logger = logging.getLogger(__name__)


class BaseLdap3(object):
    def __init__(
            self, host='localhost', port=389, use_ssl=False, allowed_referral_hosts=None, get_info=ldap3.SCHEMA,
            mode=ldap3.IP_SYSTEM_DEFAULT, tls=None, formatter=None, connect_timeout=60,
            user=None, password=None, auto_bind=True, client_strategy=ldap3.SAFE_SYNC, receive_timeout=60,
    ):

        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.allowed_referral_hosts = allowed_referral_hosts
        self.get_info = get_info
        self.mode = mode
        self.tls = tls
        self.formatter = formatter
        self.connect_timeout = connect_timeout

        self.user = user
        self.pw = password
        self.auto_bind = auto_bind
        self.client_strategy = client_strategy
        self.receive_timeout = receive_timeout

        self.server = None
        self.conn = None

    def __enter__(self):
        try:
            self.server = Server(
                self.host, self.port, self.allowed_referral_hosts, self.get_info, self.mode,
                self.formatter, self.connect_timeout
            )
            self.conn = Connection(
                self.server, self.user, self.pw,
                auto_bind=self.auto_bind, client_strategy=self.client_strategy, receive_timeout=self.receive_timeout
            )
            if self.use_ssl:
                self.conn.start_tls(read_server_info=False)
                self.conn.bind(read_server_info=True)
            return self
        except Exception as e:
            logger.error("Failed to connect to ldap: {}".format(e))
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.unbind()

    def search(self, search_base, search_filter, search_scope, attributes, get_operational_attributes, size_limit):
        try:
            self.conn.search(
                search_base, search_filter, search_scope=search_scope, attributes=attributes,
                get_operational_attributes=get_operational_attributes, size_limit=size_limit
            )
            print(self.conn.usage)
            return self.conn.response
        except Exception:
            raise




