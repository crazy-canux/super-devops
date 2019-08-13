import libvirt
import sys
import logging

logger = logging.getLogger(__name__)
logging.getLogger('libvirt').setLevel(logging.WARNING)


class BaseLibvirt(object):

    def __init__(self, uri="qemu:///system"):
        self.uri = uri
        self.connection = None

    def __enter__(self):
        try:
            self.connection = libvirt.open(self.uri)
            if self.connection is None:
                logger.error("No connection object returned.")
                sys.exit(1)
            return self
        except Exception as e:
            logger.error("Failed to connection to qemu: {}".format(e))
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def network_exist(self, name):
        try:
            if name in self.connection.listNetworks():
                logger.debug("network {} exist.".format(name))
                return True
            else:
                logger.debug("network {} not exist.".format(name))
                return False
        except Exception as e:
            logger.error("Check network exist failed: {}".format(e))

    def create_network(self, xmlDesc):
        try:
            network = self.connection.networkCreateXML(xmlDesc)
            if network is None:
                logger.error("No network created.")
                return False
            logger.debug(network.autostart())
            logger.debug(network.isActive())
            logger.debug(network.isPersistent())
            return True
        except Exception as e:
            logger.error("Failed to create virtual network: {}".format(e))

    def define_network(self, xmlDesc):
        try:
            network = self.connection.networkDefineXML(xmlDesc)
            if network is None:
                logger.error("No network created.")
                return False
            network.setAutostart(1)
            network.create()
            logger.debug(network.autostart())
            logger.debug(network.isActive())
            logger.debug(network.isPersistent())
            return True
        except Exception as e:
            logger.error(
                "Failed to create and start virtual network: {}".format(e)
            )

    def undefine_network(self, name):
        try:
            network = self.connection.networkLookupByName(name)
            if network is None:
                logger.error("Network {} not exist.".format(name))
                return False
            network.undefine()
            return True
        except Exception as e:
            logger.error("Failed to remove network: {}".format(e))
            return False

    def destroy_network(self, name):
        try:
            network = self.connection.networkLookupByName(name)
            if network is None:
                logger.error("Network {} not exist.".format(name))
                return False
            network.destroy()
            return True
        except Exception as e:
            logger.error("Failed to stop network: {}".format(e))
            return False

    def undefine_all_vms(self, name):
        pass