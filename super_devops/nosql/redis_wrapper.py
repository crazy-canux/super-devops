import redis


class BaseRedis(redis.Redis):
    def __init__(
            self, host='localhost', port='6379', db=0, password=None,
            decode_responses=None, connection_pool=None, *args, **kwargs
    ):
        super(BaseRedis, self).__init__(
            host, port, db, password,
            decode_responses=decode_responses, connection_pool=connection_pool,
            *args, **kwargs
        )


if __name__ == "__main__":
    redis = BaseRedis()
    pl = redis.pipeline()
