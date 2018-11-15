"""Global Utils.

Only Python Standard Library can be used here.
"""
import os
import datetime


class Utils(object):

    @staticmethod
    def expandpath(path):
        if path:
            real_path = path
        else:
            return None
        if '~' in path:
            real_path = os.path.expanduser(path)
        if '$' in path:
            real_path = os.path.expandvars(path)
        return real_path

    @staticmethod
    def file_2_sql(filename):
        """Remove go from sql file for sqlalchemy and pymssql."""
        with open(filename, 'rb') as f:
            sql_list = f.readlines()
            sql_list = [
                line
                for line in sql_list
                if
                line.strip() not in ['go', 'GO', 'Go', 'gO'] and line.strip()
            ]
            sql = "".join(sql_list)
        return sql

    @staticmethod
    def timestamp():
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

