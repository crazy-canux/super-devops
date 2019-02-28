.. _amqp:

pika
====

`<https://github.com/pika/pika>`_

install
-------

install from pypi::

    $ pip install pika

usage
-----

import::

    import pika

Class BlockingConnection::

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            self.host,
            self.port,
            self.virtual_host,
            self.credentials,
            **self.kwargs
        )
    )
    connection = pika.BlockingConnection(
        pika.URLParameters(
            "amqp://username:password@host:port/<virtual_host>[?query-string]"
            # eg: "amqp://guest:guest@localhost:5672/%2F"
            # "amqp://user:passwd@host:port/vhost?connection_attempts=10&retry_delay=3"
        )
    )

    # methods
    channel = connection.channel() # return BlockingChannel object.
    connection.close()

    # data
    is_closed
    is_closing
    is_open

Class BasicProperties::

         BasicProperties(content_type=None,content_encoding=None, headers=None,
         delivery_mode=None, priority=None, correlation_id=None, reply_to=None,
         expiration=None, message_id=None, timestamp=None, type=None,
         user_id=None, app_id=None, cluster_id=None)

         content_type:
         "application/json"

         delivery_mode:
         2: data persistent

         priority:

Class BlockingChannel::

    BlockingChannel(channel_impk, connection)

    # methods
    basic_publish(exchange, routing_key, body, properties=None,mandatory=False, immediate=False) # producer
    > properties = pika.BasicProperties(...)

    basic_consume(consumer_callback, queue, no_ack=False, exclusive=False,consumer_tag=None, arguments=None) # consumer.
    > consumer_callback = function_name(channel, method, properties, body)

    basic_qos(callback=None, prefetch_size=0, prefetch_count=0,all_channels=False)
    basic_ack(delivery_tag=0, multiple=False) # acknowledge messages.
    basic_cancel(consumer_tag) # cancels consumer.
    basic_get(queue=None, no_ack=False)
    basic_nack(...)
    basic_recover(...)
    basic_reject(...)
    cancel()
    consume(...)
    close(reply_code=0, reply_text="Normal shutdown")
    confirm_delivery(callback=None, nowait=False)
    exchange_declare(exchange=None, exchange_type='direct', passive=False,durable=False, auto_delete=False, internal=False, arguments=None)
    exchange_bind(destination=None, source=None, routing_key='',arguments=None)
    exchange_unbind(destination=None, source=None, routing_key='',arguments=None)
    exchange_delete(exchange=None, if_unused=False)
    publish()
    queue_declare(queue='', passive=False, durable=False, exclusive=False,auto_delete=False)
    queue_bind(queue, exchange, routing_key=None, arguments=None)
    queue_unbind(queue='', exchange=None, routing_key='', arguments=None)
    queue_delete(queue='', if_unused=False, if_empty=False)
    queue_purge(queue='')
    start_consuming() # consumer start consumer message.
    stop_consuming(consumer_tag=None) # consumer stop consume message.

    # data
    channel_number

