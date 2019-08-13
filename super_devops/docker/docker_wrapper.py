import logging

import docker

logger = logging.getLogger(__name__)
logging.getLogger('docker').setLevel(logging.WARNING)


class BaseDocker(object):
    def __init__(
            self, base_url='unix://var/run/docker.sock',
            version="auto", timeout=60, **kwargs
    ):
        self.base_url = base_url
        self.version = version
        self.timeout = timeout
        self.kwargs = kwargs

        self.client = None

    def __enter__(self):
        try:
            self.client = docker.DockerClient(
                self.base_url, version=self.version, timeout=self.timeout,
                **self.kwargs
            )
            if self.client is None:
                logger.error("No connection object returned.")
                raise Exception("Connection failed.")
            return self
        except Exception as e:
            logger.error("Failed to connection to dockerd: {}".format(e))
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def info(self):
        try:
            info = self.client.info()
        except Exception as e:
            logger.error("Docker Info failed: {}".format(e))
            raise e
        else:
            # return dict.
            return info

    def ping(self):
        try:
            result = self.client.ping()
        except Exception as e:
            logger.error("Docker Server not avaliable: {}".format(e))
            raise e
        else:
            # return bool
            return result

    def login(
            self, username, password, email="canuxcheng@gmail.com",
            registry='https://index.docker.io/v1/',
            reauth=True, dockercfg_path="$HOME/.docker/config.json"
    ):
        try:
            res = self.client.login(
                username, password, email, registry, reauth, dockercfg_path
            )
        except Exception as e:
            logger.error("Docker Login failed: {}".format(e))
            raise e
        else:
            # return dict
            return res


class BaseSwarm(object):
    def __init__(
            self, base_url='unix://var/run/docker.sock',
            version="auto", timeout=60, **kwargs
    ):
        self.base_url = base_url
        self.version = version
        self.timeout = timeout
        self.kwargs = kwargs

        self.swarm = None

    def __enter__(self):
        try:
            self.client = docker.DockerClient(
                self.base_url, version=self.version, timeout=self.timeout,
                **self.kwargs
            )
            if self.client is None:
                logger.error("No connection object returned.")
                raise Exception("Connection failed.")
            self.swarm = self.client.swarm
            return self
        except Exception as e:
            logger.error("Failed to connection to dockerd: {}".format(e))
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def init(
            self, advertise_addr=None, force_new_cluster=True,
            default_addr_pool=["10.0.0.0/8"],
            subnet_size=None, listen_addr='0.0.0.0:2377',
            **kwargs
    ):
        try:
            node_id = self.swarm.init(
                advertise_addr=advertise_addr, listen_addr=listen_addr,
                force_new_cluster=force_new_cluster,
                default_addr_pool=default_addr_pool,
                subnet_size=subnet_size, **kwargs
            )
        except Exception as e:
            logger.error("Docker Swarm init failed: {}".format(e))
            raise e
        else:
            return node_id

    def join(
            self, remote_addrs=None, join_token=None, advertise_addr=None,
            listen_addr='0.0.0.0:2377', **kwargs
    ):
        try:
            result = self.swarm.join(
                remote_addrs=remote_addrs, join_token=join_token,
                listen_addr=listen_addr, advertise_addr=advertise_addr,
                **kwargs
            )
        except Exception as e:
            logger.error("Docker Swarm join failed: {}".format(e))
            raise e
        else:
            # return True
            return result

    def leave(self, force=True):
        try:
            result = self.swarm.leave(force=force)
        except Exception as e:
            logger.error("Docker Swarm leave failed: {}".format(e))
            raise e
        else:
            # return True
            return result


class BaseNetworks(object):
    def __init__(
            self, base_url='unix://var/run/docker.sock',
            version="auto", timeout=60, **kwargs
    ):
        self.base_url = base_url
        self.version = version
        self.timeout = timeout
        self.kwargs = kwargs

        self.networks = None

    def __enter__(self):
        try:
            self.client = docker.DockerClient(
                self.base_url, version=self.version, timeout=self.timeout,
                **self.kwargs
            )
            if self.client is None:
                logger.error("No connection object returned.")
                raise Exception("Connection failed.")
            self.networks = self.client.networks
            return self
        except Exception as e:
            logger.error("Failed to connection to dockerd: {}".format(e))
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    @staticmethod
    def get_ipam_pool(
            subnet=None, iprange=None, gateway=None, aux_addresses=None
    ):
        try:
            ipam_pool = docker.types.IPAMPool(
                subnet=subnet, iprange=iprange, gateway=gateway,
                aux_addresses=aux_addresses
            )
        except Exception as e:
            logger.error("Get ipam pool failed: {}".format(e))
            raise e
        else:
            return ipam_pool

    @staticmethod
    def get_ipam_config(
            driver="default", pool_configs=None, options=None
    ):
        try:
            ipam_config = docker.types.IPAMConfig(
                driver=driver, pool_configs=pool_configs, options=options
            )
        except Exception as e:
            logger.error("Get IPAM config failed: {}".format(e))
            raise e
        else:
            return ipam_config

    def create(
            self, name=None, driver="bridge", scope="local", ipam=None,
            check_duplicate=False, internal=False, enable_ipv6=False,
            attachable=False, ingress=False, options=None, labels=None
    ):
        try:
            network = self.networks.create(
                name=name, driver=driver, options=options, ipam=ipam,
                check_duplicate=check_duplicate, internal=internal,
                labels=labels, enable_ipv6=enable_ipv6, attachable=attachable,
                scope=scope, ingress=ingress
            )
        except Exception as e:
            logger.error("Docker network create failed: {}".format(e))
            raise e
        else:
            # return Network object
            return network

    def create_bridge_network(
            self, name, subnet, iprange, gateway, opt_name, opt_icc, opt_im,
            attachable
    ):
        try:
            pool_config = self.get_ipam_pool(
                subnet, iprange, gateway
            )
            ipam_config = self.get_ipam_config(
                driver="default", pool_configs=[pool_config], options=None
            )
            bridge = self.create(
                name=name, driver="bridge", ipam=ipam_config,
                check_duplicate=True, internal=False, attachable=attachable,
                ingress=False, enable_ipv6=False, scope="local",
                options={
                    "com.docker.network.bridge.enable_icc": opt_icc,
                    "com.docker.network.bridge.enable_ip_masquerade": opt_im,
                    "com.docker.network.bridge.name": opt_name
                },
                labels=None
            )
        except Exception as e:
            logger.error("Create bridge network failed: {}".format(e))
            raise e
        else:
            return bridge

    def create_overlay_network(
            self, name, subnet, iprange, gateway, opt_name
    ):
        try:
            pool_config = self.get_ipam_pool(
                subnet, iprange, gateway, aux_addresses=None
            )
            ipam_config = self.get_ipam_config(
                driver="default", pool_configs=[pool_config], options={}
            )
            overlay = self.create(
                name=name, driver="overlay", ipam=ipam_config,
                check_duplicate=True, internal=False, attachable=True,
                ingress=False, enable_ipv6=False, scope="swarm",
                options={
                    "com.docker.network.bridge.name": opt_name
                },
                labels={},
            )
        except Exception as e:
            logger.error("Create bridge network failed: {}".format(e))
            raise e
        else:
            return overlay

    def prune(self, filters=None):
        try:
            networks = self.networks.prune(filters)
        except Exception as e:
            logger.error("Docker Network prune failed: {}".format(e))
            raise e
        else:
            # return dict
            return networks

    def delete(self, names=None, ids=None, filters=None, greedy=False):
        try:
            nets = self.networks.list(
                names=names, ids=ids, filters=filters, greedy=greedy
            )
            for net in nets:
                for container in net.containers:
                    logger.debug(
                        "Disconnect {} from {}".format(
                            container.name, net.name)
                    )
                    net.disconnect(container.name, force=True)
                logger.debug(
                    "Remove docker network {}:{}".format(net.id, net.name)
                )
                net.remove()
        except Exception as e:
            logger.error("Docker Network delete failed: {}".format(e))
            raise e
        else:
            return True

    def list(self, names=None, ids=None, filters=None, greedy=False):
        try:
            nets = self.networks.list(
                names=names, ids=ids, filters=filters, greedy=greedy
            )
        except Exception as e:
            logger.error("Docker Network list failed: {}".format(e))
            raise e
        else:
            return nets


class BaseImages(object):
    def __init__(
            self, base_url='unix://var/run/docker.sock',
            version="auto", timeout=60, **kwargs
    ):
        self.base_url = base_url
        self.version = version
        self.timeout = timeout
        self.kwargs = kwargs

        self.images = None

    def __enter__(self):
        try:
            self.client = docker.DockerClient(
                self.base_url, version=self.version, timeout=self.timeout,
                **self.kwargs
            )
            if self.client is None:
                logger.error("No connection object returned.")
                raise Exception("Connection failed.")
            self.images = self.client.images
            return self
        except Exception as e:
            logger.error("Failed to connection to dockerd: {}".format(e))
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def load(self, data):
        try:
            images = self.images.load(data)
        except Exception as e:
            logger.error("Docker Image load failed: {}".format(e))
            raise e
        else:
            # return list of Images
            return images

    def list(self, name=None, if_all=False, filters=None):
        try:
            images = self.images.list(name, if_all, filters)
        except Exception as e:
            logger.error("Docker Image list failed: {}".format(e))
            raise e
        else:
            # return list
            return images

    def prune(self, filters=None):
        try:
            images = self.images.prune(filters)
        except Exception as e:
            logger.error("Docker Image prune failed: {}".format(e))
            raise e
        else:
            # return dict
            return images

    def remove(
            self, image=None, force=False, noprune=False
    ):
        try:
            self.images.remove(image, force, noprune)
        except Exception as e:
            logger.error("Docker Image remove failed: {}".format(e))
            raise e

    def delete_all(self):
        try:
            for image in self.list(if_all=True):
                self.images.remove(image.id)
        except Exception as e:
            logger.error("Docker Image delete failed: {}".format(e))
            raise e


class BaseVolumes(object):
    def __init__(
            self, base_url='unix://var/run/docker.sock',
            version="auto", timeout=60, **kwargs
    ):
        self.base_url = base_url
        self.version = version
        self.timeout = timeout
        self.kwargs = kwargs

        self.volumes = None

    def __enter__(self):
        try:
            self.client = docker.DockerClient(
                self.base_url, version=self.version, timeout=self.timeout,
                **self.kwargs
            )
            if self.client is None:
                logger.error("No connection object returned.")
                raise Exception("Connection failed.")
            self.volumes = self.client.volumes
            return self
        except Exception as e:
            logger.error("Failed to connection to dockerd: {}".format(e))
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def prune(self):
        try:
            volumes = self.volumes.prune(filters=None)
        except Exception as e:
            logger.error("Docker Volumes prune failed: {}".format(e))
            raise e
        else:
            # return dict
            return volumes


class BaseContainers(object):
    def __init__(
            self, base_url='unix://var/run/docker.sock',
            version="auto", timeout=60, **kwargs
    ):
        self.base_url = base_url
        self.version = version
        self.timeout = timeout
        self.kwargs = kwargs

        self.containers = None

    def __enter__(self):
        try:
            self.client = docker.DockerClient(
                self.base_url, version=self.version, timeout=self.timeout,
                **self.kwargs
            )
            if self.client is None:
                logger.error("No connection object returned.")
                raise Exception("Connection failed.")
            self.containers = self.client.containers
            return self
        except Exception as e:
            logger.error("Failed to connection to dockerd: {}".format(e))
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def prune(self):
        try:
            containers = self.containers.prune(filters=None)
        except Exception as e:
            logger.error("Docker Containers prune failed: {}".format(e))
            raise e
        else:
            # return dict
            return containers

    def list(
            self, all=False, since=None, before=None, limit=None,
            filters=None, sparse=False, ignore_removed=False
    ):
        try:
            containers = self.containers.list(
                all, since, before, limit, filters, sparse, ignore_removed
            )
        except Exception as e:
            logger.error("Docker Containers list failed: {}".format(e))
            raise e
        else:
            return containers

    def delete_all(self):
        try:
            for container in self.list(all=True):
                logger.debug("delete container: {}".format(container.name))
                container.stop()
                container.remove()
        except Exception as e:
            logger.error(
                "Docker Container delete(stop/remove) failed: {}".format(e)
            )
            raise e


class BaseServices(object):
    def __init__(
            self, base_url='unix://var/run/docker.sock',
            version="auto", timeout=60, **kwargs
    ):
        self.base_url = base_url
        self.version = version
        self.timeout = timeout
        self.kwargs = kwargs

        self.services = None

    def __enter__(self):
        try:
            self.client = docker.DockerClient(
                self.base_url, version=self.version, timeout=self.timeout,
                **self.kwargs
            )
            if self.client is None:
                logger.error("No connection object returned.")
                raise Exception("Connection failed.")
            self.services = self.client.services
            return self
        except Exception as e:
            logger.error("Failed to connection to dockerd: {}".format(e))
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def list(self, filters=None):
        try:
            services = self.services.list(filters=filters)
        except Exception as e:
            logger.error("Docker Service list failed: {}".format(e))
            raise e
        else:
            # return list
            return services


class BaseNodes(object):
    def __init__(
            self, base_url='unix://var/run/docker.sock',
            version="auto", timeout=60, **kwargs
    ):
        self.base_url = base_url
        self.version = version
        self.timeout = timeout
        self.kwargs = kwargs

        self.nodes = None

    def __enter__(self):
        try:
            self.client = docker.DockerClient(
                self.base_url, version=self.version, timeout=self.timeout,
                **self.kwargs
            )
            if self.client is None:
                logger.error("No connection object returned.")
                raise Exception("Connection failed.")
            self.nodes = self.client.nodes
            return self
        except Exception as e:
            logger.error("Failed to connection to dockerd: {}".format(e))
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def list(self, filters=None):
        try:
            nodes = self.nodes.list(filters=filters)
        except Exception as e:
            logger.error("Docker Node list failed: {}".format(e))
            raise e
        else:
            # return list
            return nodes




