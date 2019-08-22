import unittest
import re

from super_devops.container.docker_wrapper import BaseSwarm, BaseNetworks, \
    BaseDocker, BaseImages, BaseContainers, BaseNodes

from super_devops.ssh.paramiko_wrapper import BaseParamiko


class DockerTestCase(unittest.TestCase):

    @unittest.skip("ignore")
    def test_docker_client(self):
        with BaseDocker() as docker:
            print(docker.info())
            result = docker.ping()
        self.assertTrue(result, "ping failed")

    @unittest.skip("ignore")
    def test_swarm_leave(self):
        with BaseSwarm() as swarm:
            result = swarm.leave()
        self.assertTrue(result, "swarm leave failed.")

    @unittest.skip("ignore")
    def test_gwbridge(self):
        name = "docker_gwbridge"
        subnet = "172.18.0.0/16"
        iprange = "172.18.0.0/24"
        gateway = "172.18.0.1"
        opt_name = "docker_gwbridge"
        with BaseNetworks() as network:
            result = network.delete([name], greedy=True)
            bridge = network.create_bridge_network(
                name, subnet, iprange, gateway, opt_name,
                opt_icc="true", opt_im="true", attachable=False
            )
        print(bridge.name)
        self.assertTrue(result, "delete failed")
        self.assertEqual(name, bridge.name, "create gwbridge failed.")

    @unittest.skip("ignore")
    def test_swarm_init(self):
        node_id = None
        with BaseSwarm() as swarm:
            node_id = swarm.init(
                advertise_addr="10.103.239.40", force_new_cluster=True
            )
        print(node_id)
        self.assertIsNotNone(node_id, "swarm init failed")

    @unittest.skip("ignore")
    def test_swarm_join(self):
        with BaseParamiko(
                hostname="10.103.239.40", username="canux",
                password="S0nicwall"
        ) as ssh:
            output, error, rc = ssh.exec_command(
                "docker swarm join-token -q worker"
            )
        token = output[0].strip()
        print(token)
        with BaseSwarm() as swarm:
           result = swarm.join(
                remote_addrs=["10.103.239.40:2377"],
                join_token=token, advertise_addr="10.103.239.40"
            )
        self.assertTrue(result, "swarm join failed.")

    @unittest.skip("ignore")
    def test_overlay(self):
        name = "ol0"
        subnet = "172.12.0.0/16"
        iprange = "172.12.0.0/24"
        gateway = "172.12.0.1"
        opt_name = "ol0"
        with BaseNetworks() as network:
            result = network.create_overlay_network(
                name=name, subnet=subnet, iprange=iprange, gateway=gateway,
                opt_name=opt_name
            )
        print(result.name)
        self.assertEqual(name, result.name, "create overlay failed")

    @unittest.skip("ignore")
    def test_get_captureatp_version(self):
        registry = "harbor.domain.com:4433"
        project = "captureatp"
        name = "sandboxav"
        repo = "{}/{}/{}".format(registry, project, name)
        with BaseImages() as image:
            images = image.list(repo, if_all=True)
            tags = [
                tag.replace(repo + ":", "")
                for one in images
                for tag in one.tags
            ]
        print(tags)

        versions = [
            tag
            for tag in tags
            if re.match("^\d.\d.\d$", tag)
        ]
        versions.sort()
        print(versions[-1])

    def test_docker_node(self):
        with BaseNodes() as n:
            nodes = n.list()
        ip = nodes[0].attrs["Status"]["Addr"]
        print(ip)
        print(type(ip))


if __name__ == '__main__':
    unittest.main()
