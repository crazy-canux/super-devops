import unittest

from super_devops.database.sqlalchemy_wrapper import BaseDB


class DatabaseTestCase(unittest.TestCase):
    def test_select_query(self):
        with BaseDB(
                host='127.0.0.1', username='username',
                password='password', database='test', port=1433
        ) as db:
            results, keys = db.select_query("select @@version")
        self.assertIsInstance(results, list, msg='results failed')
        self.assertIsInstance(keys, list, msg='keys failed')

    def test_mysql(self):
        with BaseDB(
            host='127.0.0.1', username='username',
            password='password', database='sandbox', port=3306
        ) as db:
            results, keys = db.select_query("select version();")
        self.assertIsInstance(results, list, msg='results failed')
        self.assertIsInstance(keys, list, msg='keys failed')

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

    @unittest.skip('ignore')
    def test_dml_query(self):
        with BaseDB(
                host='127.0.0.1', username='username',
                password='password', database='test', port=1433
        ) as db:
            result = db.dml_query("delete from table where key = "
                                  "'value'")
            result1 = db.dml_query("update table set key = 'value' where "
                                   "key = 'value'")


if __name__ == '__main__':
    unittest.main()
