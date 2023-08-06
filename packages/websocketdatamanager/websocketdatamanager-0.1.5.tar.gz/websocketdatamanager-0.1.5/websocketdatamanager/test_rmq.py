from rmq_engine import RMQEngine
from queue import Queue

if __name__ == "__main__":
    queue2ws = Queue()
    amqp_data = {
        'amqp': True,
        'code': 'status',
        'vhost': "gpsdata",
        'host': "10.54.217.95",
        'credentials': ("enugeojson_prod",
                        "geognss_prod"),
        'queue_name': 'status_gnss',
        'routing_key': 'status',
        'exchange': 'status_exchange',
        'durable': True,
        'queue2ws': queue2ws,
        'consumer_tag': 'mq2ws'
    }
    rmq = RMQEngine(**amqp_data)
    rmq.cycle()
