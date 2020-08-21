import ipaddress
import logging
import sys

import pyroute2

logger = logging.getLogger(__name__)


def get_netmask(address, prefixlen, with_enable=False):
    """
    address/prefixlen = '192.168.168.0/24'
    netmask: 255.255.255.0
    with_netmask: 192.168.168.0/255.255.255.0
    """
    info = ipaddress.ip_network("{}/{}".format(address, prefixlen))
    if with_enable:
        return info.with_netmask
    else:
        return str(info.netmask)


def get_prefixlen(address, netmask, with_enable=True):
    """
    address/netmask = '192.168.168.0/255.255.255.0'
    with_prefixlen: 192.168.168.0/24
    prefixlen: 24
    """
    info = ipaddress.ip_network("{}/{}".format(address, netmask))
    if with_enable:
        return info.with_prefixlen
    else:
        return info.prefixlen


class BaseIP(object):
    def __init__(self, interface=None, address=None, netmask=None, gateway=None, subnet=None):
        self.interface = interface
        self.address = address
        self.netmask = netmask
        self.gateway = gateway
        self.subnet = subnet

        self.ip = None

    def __enter__(self):
        try:
            self.ip = pyroute2.IPRoute()
            if self.ip is None:
                logger.error("No route object returned.")
                sys.exit(1)
            return self
        except Exception as e:
            logger.error("Failed to init route object: {}".format(e))
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ip.close()

    def get_route(self, family=2, table=254, dst=None, prefsrc=None, gateway=None, oif=None):
        """
        family: socket.AF_UNSPEC/0, AF_UNIX/1, AF_INET/2, ...

        (
        {'event': 'RTM_NEWROUTE', 'scope': 253, 'table': 254, 'family': 2, 'proto': 2, 'type': 1, 'flags': 16, 'tos': 0, 'src_len': 0, 'dst_len': 24,
        'header': {'pid': 6908, 'target': 'localhost', 'error': None, 'sequence_number': 273, 'type': 24, 'flags': 2, 'length': 60, 'stats': Stats(qsize=0, delta=0, delay=0)},
        'attrs': [('RTA_TABLE', 254), ('RTA_GATEWAY', '10.103.64.1'), ('RTA_DST', '192.168.168.0'), ('RTA_PREFSRC', '192.168.168.168'), ('RTA_OIF', 2)]
        },
        )
        mask = r['dst_len']
        destination = dict(r['attrs'])["RTA_DST"]
        """
        if oif:
            oif = oif
        elif self.interface:
            oif = self.ip.link_lookup(ifname=self.interface)[0]
        routes = self.ip.route("dump", family=family, table=table, dst=dst, prefsrc=prefsrc, gateway=gateway, oif=oif)
        logger.debug("routes: {}".format(routes))
        return routes

    def add_route(self, destination, prefsrc=None, gateway="0.0.0.0", oif=None, family=2, table=254, scope=None, proto=None):
        """
        dst = "ip/len" equal to dst = "ip", dst_len="len"

        :param gateway: 0.0.0.0(default), if not specify
        :param family: 10|inet6 / 2|inet (ref: import socket)
        :param table: 253|default / 254|main / 255|local / 0|unspec
        :param destination:
        :param oif:
        :param prefsrc:
        :param scope: 0|global(default) / 253|link / 254|host / 255|nowhere / 200|site
        :param proto: 4|static(default) / 0|unspec / 1|redirect / 2|kernel / 3|boot
        :return:
        """
        try:
            if oif:
                oif = oif
            elif self.interface:
                oif = self.ip.link_lookup(ifname=self.interface)[0]
            self.ip.route(
                "add",
                family=family, table=table, proto=proto, scope=scope,
                dst=destination, prefsrc=prefsrc, gateway=gateway,
                oif=oif
            )
        except Exception as e:
            logger.error("ip route add  failed: {}".format(e.args))
            return False
        else:
            return True

    def delete_route(self, destination, prefsrc=None, gateway="0.0.0.0", oif=None, family=2, table=254, scope=None, proto=None):
        try:
            if oif:
                oif = oif
            elif self.interface:
                oif = self.ip.link_lookup(ifname=self.interface)[0]
            self.ip.route(
                "del",
                family=family, table=table, proto=proto, scope=scope,
                dst=destination, prefsrc=prefsrc, gateway=gateway,
                oif=oif
            )
        except Exception as e:
            logger.error("ip route delete failed: {}".format(e.args))
            return False
        else:
            return True

    def get_link(self):
        return self.ip.link("get", index=self.ip.link_lookup(ifname=self.interface)[0])

    def add_link(self, kind, address, link=None, index=None, name=None, broadcast=None, mtu=1500, state="up"):
        """
        ip link add [ link DEVICE ] [ name ] NAME [args] type TYPE [ ARGS ]
        ip link set { DEVICE | group GROUP } { up | down [args]

        family: 0
        type: 1

        type/kind = { vlan | veth | vcan | dummy | ifb | macvlan | macvtap |
          bridge | bond | ipoib | ip6tnl | ipip | sit | vxlan |
          gre | gretap | ip6gre | ip6gretap | vti | nlmon |
          bond_slave | ipvlan | geneve | bridge_slave | vrf }
        :return:
        """
        try:
            self.ip.link(
                "add", ifname=self.interface, kind=kind, address=address, broadcast=broadcast, mtu=mtu,
                link=link, index=index
            )
            self.ip.link(
                "set", index=self.ip.link_lookup(ifname=self.interface)[0], state=state, name=name
            )
        except Exception as e:
            logger.error("ip link add failed: {}".format(e.args))
            return False

    def set_link(self, state='up', name=None):
        try:
            self.ip.link("set", index=self.ip.link_lookup(ifname=self.interface)[0], state=state, name=name)
        except Exception as e:
            logger.error("ip link set failed: {}".format(e.args))
            return False
        else:
            return True

    def delete_link(self):
        """ip link delete { DEVICE | dev DEVICE | group DEVGROUP } type TYPE [ ARGS ]"""
        try:
            self.ip.link("del", index=self.ip.link_lookup(ifname=self.interface)[0])
        except Exception as e:
            logger.error("ip link delete failed: {}".format(e.args))

    def flush_address(self):
        try:
            self.ip.flush_addr(index=self.ip.link_lookup(ifname=self.interface)[0])
        except Exception as e:
            logger.error("ip addr flush failed: {}".format(e.args))
            return False
        else:
            return True

    def add_address(self, address, prefixlen, broadcast=None, ):
        try:
            self.ip.addr(
                "add", index=self.ip.link_lookup(ifname=self.interface)[0], address=address, prefixlen=prefixlen,
                broadcast=broadcast,
            )
        except Exception as e:
            logger.error("ip addr add failed: {}".format(e.args))
            return False
        else:
            return True

    def delete_address(self):
        try:
            self.ip.addr(
                "del", index=self.ip.link_lookup(ifname=self.interface)[0]
            )
        except Exception as e:
            logger.error("ip addr delete failed: {}".format(e.args))
            return False
        else:
            return True


class BaseNDB(object):
    def __init__(self, interface, address=None, netmask=None, gateway=None, subnet=None):
        self.interface = interface
        self.address = address
        self.netmask = netmask
        self.gateway = gateway
        self.subnet = subnet

        self.ndb = None

    def __enter__(self):
        try:
            self.ndb = pyroute2.NDB()
            if self.ndb is None:
                logger.error("No ndb object returned.")
                sys.exit(1)
            return self
        except Exception as e:
            logger.error("Failed to init ndb object: {}".format(e))
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ndb.close()
