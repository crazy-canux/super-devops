import unittest
import logging
import os
import hashlib

from super_devops.container.registry_wrapper import BaseRegistry


logger = logging.getLogger(__name__)


class RegistryTestCase(unittest.TestCase):

    def test_docker_client(self, image):
        try:
            name = image.split("/")[1:][0] + "/" + image.split("/")[1:][1].split(":")[0]
            tag = image.split(":")[-1]
            registry = "/path/to/registry"

            harbor = "https://harbor.domain.com"
            user = "username"
            pw = "password"
            reg = BaseRegistry(harbor, user, pw)

            manifests_file = os.path.join(registry, "manifests", name, tag)
            logger.debug(manifests_file)
            m_resp = reg.get_manifests(name, tag)
            manifests = m_resp.json()
            if os.path.isfile(manifests_file):
                logger.debug("{} already exist.".format(manifests_file))
            else:
                os.makedirs(os.path.dirname(manifests_file), exist_ok=True)
                sha256 = hashlib.sha256()
                with open(manifests_file, "wb") as f:
                    for chunk in m_resp.iter_content(512 * 1024):
                        sha256.update(chunk)
                        f.write(chunk)
                if m_resp.headers['Docker-Content-Digest'] != "sha256:{}".format(sha256.hexdigest()):
                    os.remove(manifests_file)
                    raise Exception("sha256 not match when get image manifests: {}:{}".format(name, tag))

            img_sha256 = manifests["config"]["digest"]
            image_file = os.path.join(registry, "blobs", img_sha256)
            logger.debug(image_file)
            if os.path.isfile(image_file):
                logger.debug("{} already exist.".format(image_file))
            else:
                os.makedirs(os.path.dirname(image_file), exist_ok=True)
                b_resp = reg.get_blobs(name, img_sha256)
                if img_sha256 != b_resp.headers['Docker-Content-Digest']:
                    raise Exception("sha256 not match when get image blobs: {}".format(img_sha256))
                with open(image_file, 'wb') as f:
                    for chunk in b_resp.iter_content(512 * 1024):
                        f.write(chunk)

            for layer in manifests["layers"]:
                layer_sha256 = layer["digest"]
                blobs_file = os.path.join(registry, "blobs", layer_sha256)
                logger.debug(blobs_file)
                if os.path.isfile(blobs_file):
                    logger.debug("{} already exist".format(blobs_file))
                    continue
                os.makedirs(os.path.dirname(blobs_file), exist_ok=True)
                blobs = reg.get_blobs(name, layer_sha256)
                if blobs.headers['Docker-Content-Digest'] != layer_sha256:
                    raise Exception("sha256 not match when get blobs: {}".format(layer_sha256))
                with open(blobs_file, 'wb') as f:
                    for chunk in blobs.iter_content(512 * 1024):
                        f.write(chunk)
        except Exception:
            raise


if __name__ == '__main__':
    unittest.main()
