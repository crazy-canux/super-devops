import unittest
from super_devops.vault import BaseVault


class VaultTestCase(unittest.TestCase):
    server = "http://127.0.0.1:8200"
    vault = BaseVault(server=server)
    if not vault.health():
        token_key = vault.init()
        token = token_key["root_token"]
        keys = token_key["keys"]
        for key in keys[:3]:
            vault.unseal(key)
        vault.enable_kv2(token=token, path="test")
        vault.create_policy(token=token, name="test", path="test")
        config_capture(server, token)
        vault.seal(token=token)
    else:
        print("already initialized.")


if __name__ == "__main__":
    unittest.main()
