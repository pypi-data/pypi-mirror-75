from WebsocketDataManager import WebsocketDataManager as WDM
from queue import Queue
from networktools.ip import network_ip

if __name__ == "__main__":
    queue2ws = Queue()
    queue2mq = Queue()
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
    engine_opts = {
        'status': amqp_data
    }
    ws_data = {
        'port': 8000,
        'host': network_ip(),
        'queue2ws': queue2ws,
        'delta_time': 2,
        'path': 'ws/status_all/ws_source/'
    }
    ws_opts = {'status': ws_data}
    wdm = WDM({'status': queue2ws, 'status_recv': queue2mq},
              engine_opts, ws_opts)
    wdm.task_cycle()
