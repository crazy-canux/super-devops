import unittest

from super_devops.ldap.ldap3_wrapper import BaseLdap3
import ldap3

old = "ldap://super-devops.canux.com"
new = "ldaps://super-devops.canux.com"


class LdapTestCase(unittest.TestCase):
    def test_connection(self):
        with BaseLdap3(
                old, port=389, use_ssl=False, allowed_referral_hosts=[("*", True)],
                get_info=ldap3.NONE, auto_bind=False
        ) as ldap:
            self.assertIsNotNone(ldap.conn)

    def test_search(self):
        with BaseLdap3(
                new, port=636, use_ssl=True, allowed_referral_hosts=[("*", True)],
                get_info=ldap3.NONE, auto_bind=False
        ) as ldap:
            filters = '(&(objectClass=inetOrgPerson)(username=canux))'
            a = ldap.search('ou=people,dc=arm,dc=com', filters, ldap3.SUBTREE, ldap3.ALL_ATTRIBUTES, True, 1)


if __name__ == "__main__":
    unittest.main()
