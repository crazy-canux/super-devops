import unittest

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.database.sqlalchemy_wrapper import BaseDB


class ParamikoTest(unittest.TestCase):
    def test_select_query(self):
        with BaseDB(
                host='10.103.239.70', username='sandbox',
                password='P@ssword', database='sandbox', port=1433
        ) as db:
            result = db.select_query("select * from units")
        print result

    @unittest.skip('ignore')
    def test_sql_file(self):
        with open('../data/test.sql', 'rb') as f:
            sql_list = f.readlines()
        sql_list = [
            line
            for line in sql_list
            if line.strip() != 'go'
        ]
        sql = ";".join(sql_list)
        print("sql: {}".format(sql))
        with BaseDB(
                host='10.103.239.70', username='sandbox',
                password='P@ssword', database='sandbox', port=1433
        ) as db:
            result = db.execute_transaction(sql)
        if result:
            print("Succeed.")
        else:
            print("Failed.")

if __name__ == '__main__':
    unittest.main()
