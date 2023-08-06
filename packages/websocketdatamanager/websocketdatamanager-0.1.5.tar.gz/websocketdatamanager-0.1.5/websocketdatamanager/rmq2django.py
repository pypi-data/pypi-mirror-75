#!/home/david/.virtualenvs/wsdata/bin/python

from asyncio import Queue
from DjangoDataManager import DjangoDataManager as DJDM
from networktools.ip import network_ip
from networktools.environment import get_env_variable

if __name__ == "__main__":
    # async queue
    # doc: https://docs.python.org/3.6/library/asyncio-queue.html
    queue2dj = Queue()
    queue2mq = Queue()
    # datos de conexión a la cola rmq
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
        'queue2dj': queue2dj,
        'consumer_tag': 'mq2ws'
    }
    # esto activa los channels en la clase
    engine_opts = {
        'status': amqp_data
    }
    # los datos de conexión adonde se envían
    dj_data = {
        'port': get_env_variable("PORT", datatype=int),
        'host': get_env_variable("HOST"),
        'queue2ws': queue2ws,
        'delta_time': 2,
        'path': 'ws/status_all/ws_source/'
    }
    dj_opts = {'status': dj_data}
    djdm = DJDM({'status': queue2dj, 'status_recv': queue2mq},
                engine_opts, dj_opts)
    djdm.task_cycle()
