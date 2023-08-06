# Contrib csn:
from data_amqp import AMQPData
from networktools.colorprint import gprint, bprint, rprint
from networktools.time import timestamp
from tasktools.taskloop import coromask, renew, simple_fargs, simple_fargs_out
# Standar lib
import math
import codecs
import logging
import asyncio
import functools as fc

from .rmq_engine import RMQEngine
from .ws_client import WSClient

"""
Contrib
"""
import ujson as json


"""
La implementación de una clase heredera

Signatures:
==========

- a :: array
- s :: string
- v :: variant
- a{sv} :: un diccionario

ref:: https://www.gkbrk.com/2018/02/simple-dbus-service-in-python/
"""


"""

DBusConnection
"""


class WebsocketDataManager:
    """
    This class pretends to create a knut in what receive data from RMQ queues and send to
    some websocket connection uri
    """

    def __init__(self, queue_set, engine_opts, ws_opts, step=0.1, *args, **kwargs):
        self.step = step
        self.queue_set = queue_set
        self.engine_opts = engine_opts
        self.ws_opts = ws_opts
        self.engine = False

    async def cycle_send_to_ws(self, *args):
        engine = args[0]
        v = args[1]
        channels = args[2]
        if v == 0:
            aux_set = set()
            for channel in channels:
                rmq = engine.get(channel)
                try:
                    rmq.amqp.connect()
                except Exception as e:
                    print("Error on connection to ws es->%s" % e)
                    v = 0
                    return engine, v, channels
                aux_set.add(channel)
            for channel in aux_set:
                channels.remove(channel)
            aux_set = None
            v += 1
            await asyncio.sleep(self.step)
            return engine, v, channels
        else:
            for channel, rmq in engine.items():
                try:

                    queue = self.queue_set.get(channel)
                    queue, active = await rmq.amqp.consume_exchange_mq(queue, True)
                except Exception as e:
                    print("Error en cycle send to ws es->%s" % e)
                    v = 0
                    channels.add(channel)
            await asyncio.sleep(self.step)
            return engine, v, channels

    async def cycle_send_to_mq(self, *args):
        engine = args[0]
        try:
            for channel, rmq in engine.items():
                queue = self.queue_set.get("%s_recv" % channel)
                if not queue.empty():
                    for i in range(queue.qsize()):
                        msg = queue.get()
                        queue.task_done()
        except Exception as e:
            print("Error en cycle send to mq es->%s" % e)
            raise e
        await asyncio.sleep(self.step)
        return args

    async def cycle_read_from_ws(self, *args):
        engine = args[0]
        channel = args[1]
        queue = self.queue_set.get(channel)
        if engine:
            if not queue.empty():
                for i in range(queue.qsize()):
                    msg = queue.get()
                    if type(msg) == dict:
                        # get channel from msg, to direct the msg
                        channel = msg.get('channel', None)
                        if channel in engine:
                            try:
                                if engine.get(channel).status:
                                    # select the dbus channel and send data
                                    engine.get(channel).enu_data(msg)
                            except Exception as ex:
                                print(ex)
                                raise ex
                    queue.task_done()
        await asyncio.sleep(self.step)
        return engine, channel

    def task_cycle(self):
        loop = asyncio.get_event_loop()
        tasks_list = []
        """
        RMQ Task
        """
        rmq_engine = {channel: RMQEngine(**value_dict)
                      for channel, value_dict in self.engine_opts.items()}
        {rmq.active_queue_switch() for rmq in rmq_engine.values()}
        channels = set([channel for channel in self.engine_opts])
        # mq 2 ws
        gprint("Engine RMQ")
        cycle_rmq_args = [rmq_engine, 0, channels]
        coroutine_future = coromask(self.cycle_send_to_ws,
                                    cycle_rmq_args,
                                    simple_fargs_out)
        task = loop.create_task(coroutine_future)
        task.add_done_callback(
            fc.partial(renew, task, self.cycle_send_to_ws, simple_fargs_out))
        tasks_list.append(task)

        """
        # ws 2 mq
        coroutine_future = coromask(self.cycle_send_to_mq,
                                    [rmq_engine],
                                    simple_fargs_out)
        task = loop.create_task(coroutine_future)
        task.add_done_callback(
            fc.partial(renew, task, self.cycle_send_to_mq, simple_fargs_out))
        tasks_list.append(task)
        """
        """
        WS read frm RMQ Task
        That could be 1 or more address
        """
        ws_engine = {channel: WSClient(**value_dict)
                     for channel, value_dict in self.ws_opts.items()}

        for channel, wsclient in ws_engine.items():
            ws_args = wsclient.get_args()+[self.queue_set.get(channel)]
            bprint("ws_args %s" % ws_args)
            # read from ws to queue
            coroutine_future = coromask(wsclient.cycle_read_from_queue,
                                        ws_args,
                                        simple_fargs_out)
            ws_task = loop.create_task(coroutine_future)
            ws_task.add_done_callback(
                fc.partial(renew, ws_task,
                           wsclient.cycle_read_from_queue,
                           simple_fargs_out))
            tasks_list.append(ws_task)
            # The read from ws to queue
            ws_args = wsclient.get_args(
            )+[self.queue_set.get("%s_recv" % channel)]
            coroutine_future = coromask(wsclient.cycle_send_to_queue,
                                        ws_args,
                                        simple_fargs_out)
            ws_task = loop.create_task(coroutine_future)
            ws_task.add_done_callback(
                fc.partial(renew, ws_task,
                           wsclient.cycle_send_to_queue,
                           simple_fargs_out))
            tasks_list.append(ws_task)
            # a heartbeat to maintain connection
            ws_task = wsclient.cycle_heartbeat(ws_args)
            tasks_list.append(ws_task)

        if not loop.is_running():
            loop.run_forever()
