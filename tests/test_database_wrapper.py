import unittest

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.database.sqlalchemy_wrapper import BaseDB


class ParamikoTestCase(unittest.TestCase):
    @unittest.skip('ignore')
    def test_select_query(self):
        with BaseDB(
                host='127.0.0.1', username='username',
                password='password', database='test', port=1433
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
                host='127.0.0.1', username='username',
                password='password', database='test', port=1433
        ) as db:
            result = db.execute_transaction(sql)
        if result:
            print("Succeed.")
        else:
            print("Failed.")

    def test_dml_query(self):
        with BaseDB(
                host='127.0.0.1', username='username',
                password='password', database='test', port=1433
        ) as db:
            result = db.dml_query("delete from jobs where sample_sha256 = "
                                  "'4ed869e5c11e23218d808f91b341f4e5fc28f729c2477f71cee956cf50dd3b16'")
            result1 = db.dml_query("update samples set status = 'bad' where "
                                   "sha256 = '4ed869e5c11e23218d808f91b341f4e5fc28f729c2477f71cee956cf50dd3b16'")
        print "delete affect:", result
        print "update affect: ", result1


if __name__ == '__main__':
    unittest.main()
