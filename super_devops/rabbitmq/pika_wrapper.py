import pika
import logging

logger = logging.getLogger(__file__)


class BaseRabbitmq(object):
    def __init__(
            self, host="localhost", port=5672, virtual_host='/',
            username='guest', password='guest', channel_max=65535,
            frame_max=131072, **kwargs
    ):
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.credentials = pika.credentials.PlainCredentials(
            username, password)

        self.channel_max = channel_max
        self.frame_max = frame_max

        # self.heartbeat = None
        # self.ssl = False
        # self.ssl_options = None
        # self.connection_attempts = 1
        # self.retry_delay = 2.0
        # self.socket_timeout = 10.0
        # self.locale = 'en_US'
        # self.backpressure_detection = False
        # self.blocked_connection_timeout = None
        # self.client_properties = None
        # self.tcp_options = None
        self.kwargs = kwargs

        self.connection = None
        self.channel = None

    def __enter__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                self.host,
                self.port,
                self.virtual_host,
                self.credentials,
                **self.kwargs
            )
        )
        self.channel = self.connection.channel()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def purge_queue(self, name):
        try:
            self.channel.queue_purge(queue=name)
        except Exception as e:
            logger.error(
                "Purge queue {} failed: {}.".format(name, e.message)
            )
            raise

    def create_exchange(
            self, exchange, exchange_type='direct', passive=False,
            durable=False, auto_delete=False, internal=False, arguments=None
    ):
        try:
            self.channel.exchange_declare(
                exchange=exchange, exchange_type=exchange_type,
                passive=passive, durable=durable, auto_delete=auto_delete,
                internal=internal, arguments=arguments
            )
        except Exception:
            raise

    def create_queue(
            self, queue, passive=False, durable=False,
            exclusive=False, auto_delete=False, arguments=None
    ):
        try:
            self.channel.queue_declare(
                queue=queue, passive=passive, durable=durable,
                exclusive=exclusive, auto_delete=auto_delete,
                arguments=arguments
            )
        except Exception:
            raise

    def bind(self, queue, exchange='', routing_key=None, arguments=None):
        try:
            self.channel.queue_bind(
                queue=queue, exchange=exchange, routing_key=routing_key,
                arguments=arguments
            )
            self.channel.confirm_delivery()
        except Exception:
            raise

    def remove_exchange(self, exchange):
        try:
            self.channel.exchange_delete(
                exchange=exchange, if_unused=False)
        except Exception:
            raise

    def remove_queue(self, queue):
        try:
            self.channel.queue_delete(
                queue=queue, if_unused=False, if_empty=False
            )
        except Exception:
            raise


if __name__ == "__main__":
    with BaseRabbitmq(
            host="localhost", username="sandbox", password="password"
    ) as mq:
        mq.create_exchange(exchange="test", durable=True)
        mq.create_queue(
            queue="canux", durable=True, arguments={"x-max-priority": 255}
        )
        mq.bind("canux", "test")
        mq.remove_exchange("test")
        mq.remove_queue("canux")



