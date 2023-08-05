# Stdlib
import json
import logging
import threading
import functools

# Pypi: Pika
import pika

# Django
from django.conf import settings
from django.db import connection as db_connection

# Project
from .config import get_config

logger = logging.getLogger(__name__)

job_methods = {}


class JobClient(object):
    def __init__(self):
        if settings.ENVIRONMENT != 'test':
            param = get_config()
            self.connection = pika.BlockingConnection(param)
            self.channel = self.connection.channel()

    def call(self, routing_key, body=None,
             exchange='default', exchange_type='direct'):
        if settings.ENVIRONMENT == 'test':
            return job_without_async(routing_key, body)

        self.channel.exchange_declare(
            exchange=exchange,
            exchange_type=exchange_type
        )

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(body, default=str),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )

    def __del__(self):
        if hasattr(self, 'channel'):
            self.connection.close()


class JobServer(object):
    job_methods = {}
    threads = []

    def __init__(self, channel, methods, connection):
        self.channel = channel
        self.job_methods = methods
        self.connection = connection

    def start(self):
        self.channel.start_consuming()

    @staticmethod
    def ack_message(ch, delivery_tag):
        """Note that `ch` must be the same pika channel instance via which
        the message being ACKed was retrieved (AMQP protocol constraint).
        """
        if ch.is_open:
            ch.basic_ack(delivery_tag=delivery_tag)
        else:
            # Channel is already closed, so we can't ACK this message;
            # log and/or do something that makes sense for your app in this case.
            pass

    @staticmethod
    def do_work(connection, ch, delivery_tag, body, func, **kwargs):
        func(body, **kwargs)
        db_connection.close()
        cb = functools.partial(JobServer.ack_message, ch, delivery_tag)
        connection.add_callback_threadsafe(cb)

    def callback(self, channel, method, properties, body):
        body = json.loads(body)

        logger.info('Start task: %s' % method.routing_key)
        queue_task = self.job_methods[method.routing_key]
        func = queue_task['func']
        kwargs = queue_task['kwargs']

        thread = threading.Thread(
            target=self.do_work,
            args=(
                self.connection,
                self.channel,
                method.delivery_tag,
                body,
                func
            ),
            kwargs=kwargs
        )
        thread.start()
        self.threads.append(thread)

        logger.info('End task: %s' % method.routing_key)

    def job_register(self):
        for key in self.job_methods.keys():
            result = self.channel.queue_declare(queue=settings.APP_NAME)
            queue_name = result.method.queue

            queue_task = self.job_methods[key]

            self.channel.exchange_declare(
                exchange=queue_task['exchange'],
                exchange_type=queue_task['exchange_type']
            )

            self.channel.queue_bind(
                exchange=queue_task['exchange'],
                queue=queue_name,
                routing_key=queue_task['routing_key']
            )

            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=self.callback
            )


def job_without_async(routing_key, body):
    if job_methods.get(routing_key):
        func = job_methods[routing_key]['func']
        data = json.dumps(body)
        func(json.loads(data))


def job_tasks(routing_key, exchange='default', exchange_type='direct',
              **kwargs):
    def wrapper(func):
        data = {
            'func': func,
            'routing_key': routing_key,
            'exchange': exchange,
            'exchange_type': exchange_type,
            'kwargs': kwargs
        }

        job_methods[routing_key] = data
        return func

    return wrapper
