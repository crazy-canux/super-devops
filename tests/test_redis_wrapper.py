import unittest

from super_devops.nosql.redis_wrapper import BaseRedis


class RedisTestCase(unittest.TestCase):
    def test_ping(self):
        redis = BaseRedis('127.0.0.1')
        print(redis.ping())

