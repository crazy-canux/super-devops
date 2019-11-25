import sys
import logging

logger = logging.getLogger(__name__)

import iptc

class BaseIptables(object):
    def __init__(self, table='filter'):
        if table.upper() == "FILTER":
            self.table_name = iptc.Table.FILTER
        elif table.upper() == "NAT":
            self.table_name = iptc.Table.NAT
        elif table.upper() == "MANGLE":
            self.table_name = iptc.Table.MANGLE
        elif table.upper() == "RAW":
            self.table_name = iptc.Table.RAW
        elif table.upper() == "SECURITY":
            self.table_name = iptc.Table.SECURITY
        else:
            raise ValueError("table not support!")
        self.table = iptc.Table(self.table_name)

    def delete_user_define_chain(self):
        try:
            logger.debug("delete all user define chain.")
            self.table.flush()
        except Exception:
            raise

    def clean_builtin_chain(self):
        try:
            logger.debug("delete all rules from builtin chain.")
            for chain in self.table.chains:
                if chain.is_builtin():
                    chain.flush()
        except Exception:
            raise

    def set_policy_for_builtin_chain(self, policy="ACCEPT"):
        try:
            logger.debug("set policy for all builtin chain.")
            for chain in self.table.chains:
                if chain.is_builtin():
                    chain.set_policy(policy.upper())
        except Exception:
            raise

    def check_rule_exist_on_chain(self, chain, rule_dict):
        try:
            chain = iptc.Chain(self.table, chain.upper())
            for rule in chain.rules:
                if iptc.easy.decode_iptc_rule(rule) == rule_dict:
                    break
            else:
                logger.debug("rule not exist.")
                return False
            logger.debug("rule exist.")
            return True
        except Exception:
            raise

    def delete_rule_from_chain(self, chain, rule_dict):
        try:
            logger.debug("delete rule from chain.")
            chain = iptc.Chain(self.table, chain.upper())
            chain.delete_rule(iptc.easy.encode_iptc_rule(rule_dict))
        except Exception:
            raise

    def replace_rule_from_chain(self, chain, rule_dict):
        try:
            logger.debug("replace rule from chain.")
            chain = iptc.Chain(self.table, chain.upper())
            chain.replace_rule(iptc.easy.encode_iptc_rule(rule_dict))
        except Exception:
            raise

    def append_rule_to_chain(self, chain, rule_dict):
        try:
            logger.debug("append rule to chain.")
            chain = iptc.Chain(self.table, chain.upper())
            chain.append_rule(iptc.easy.encode_iptc_rule(rule_dict))
        except Exception:
            raise

    def insert_rule_to_chain(self, chain, rule_dict):
        try:
            logger.debug("insert rule to chain.")
            chain = iptc.Chain(self.table, chain.upper())
            chain.insert_rule(iptc.easy.encode_iptc_rule(rule_dict))
        except Exception:
            raise


if __name__ == "__main__":
    rule_dict = {
        'src': '172.20.0.0/16',
        'dst': '!172.20.0.0/16',
        'target': 'MASQUERADE'
    }
    it = BaseIptables('nat')
    if it.check_rule_exist_on_chain('POSTROUTING', rule_dict):
        it.delete_rule_from_chain('postrouting', rule_dict)


    it = BaseIptables('filter')
    it.delete_user_define_chain()
    it.clean_builtin_chain()
    it.set_policy_for_builtin_chain()


