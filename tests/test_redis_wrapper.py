import unittest

from super_devops.nosql.redis_wrapper import BaseRedis


class RedisTestCase(unittest.TestCase):
    def test_ping(self):
        redis = BaseRedis('10.103.64.188')
        print(redis.ping())

