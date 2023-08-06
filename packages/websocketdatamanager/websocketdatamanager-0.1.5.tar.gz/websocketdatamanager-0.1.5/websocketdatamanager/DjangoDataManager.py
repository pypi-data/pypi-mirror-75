# Contrib csn:
from websocketdatamanager.rmq_engine import RMQEngine
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
from basic_queuetools.queue import read_async_queue
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async as dbaccess
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from multiprocessing import Pool
from web_dj_collector.manage import setup

setup()

from apps.station.models import InstallationEndPoint
from apps.status_unidad.models import LogUnidadGNSS

from datetime import datetime, timezone
import pytz


"""
Contrib
"""
import ujson as json
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

"""
caching installations

"""

from django.core.cache import cache
async def cache_installation(code):
    installation = cache.get("installation_%s" % code)
    if not installation:
        query_installation = await dbaccess(InstallationEndPoint.objects.filter)(
            Q(activated=True) & Q(station__code=code))
        installation = await dbaccess(query_installation.first)()        
    return installation


def crear_nuevo_log(data):
    log = LogUnidadGNSS(**data)
    return log

def save_log(log):
    log.save()

def data_save(elem):
    log = crear_nuevo_log(elem)
    log.save()
    
async def statusdata2log(station, **data):
    installation = None
    #breakpoint()
    try:
        installation = await cache_installation(station)
        if installation:
            dt_gen_time = data.get('BATT_MEM',data.get("DOP", {})).get('TIMESTAMP')
            this_time = datetime.fromtimestamp(dt_gen_time).astimezone(pytz.utc)
            data_log = {
                'installation_ep': installation,
                'dt_gen': this_time,
                'batt_cap': data.get('BATT_MEM',{}).get('BATT_CAPACITY', 0),
                'remaining_mem': data.get('BATT_MEM',{}).get('REMAINING_MEM', 0),
                'hdop': data.get('DOP',{}).get('HDOP', 20),
                'vdop': data.get('DOP',{}).get('VDOP', 20),
                'pdop': data.get('DOP',{}).get('PDOP', 20),
                'tdop': data.get('DOP',{}).get('TDOP', 20),
            }
            return data_log
    except AttributeError as ae:
        gprint("Error de atributo")
        print("No existe el atributo para el elemento", station, data, type(data), ae)
    except ObjectDoesNotExist as e:
        print("Error al cargar instalaciones", e)
        raise e


class DjangoDataManager:
    """
    This class pretends to create a knut in what receive data from RMQ queues and send directly to the objects form dj-collector on the database
    """

    def __init__(self, queue_set, engine_opts, dj_opts, step=0.1, *args, **kwargs):
        self.step = step
        self.queue_set = queue_set
        self.engine_opts = engine_opts
        self.dj_opts = dj_opts
        self.engine = False
        self.pool = Pool(processes=4)

    async def cycle_read_from_rmq(self, *args, **kwargs):
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
                    print("Error on connection to dj es->%s" % e)
                    v = 0
                    return engine, v, channels
                aux_set.add(channel)
            for channel in aux_set:
                channels.remove(channel)
            aux_set = None
            v += 1
            await asyncio.sleep(self.step)
            return [engine, v, channels], {}
        else:
            for channel, rmq in engine.items():
                try:

                    queue = self.queue_set.get(channel)
                    # breakpoint()
                    queue, active = await rmq.amqp.consume_exchange_mq(queue, True)
                except Exception as e:
                    print("Error en cycle send to dj es->%s" % e)
                    v = 0
                    channels.add(channel)
            await asyncio.sleep(self.step)
            return [engine, v, channels], {}
 
    async def cycle_send_to_dj(self, *args, **kwargs):
        """
        Leer la cola que recibe de rmq
        Enviar cada dato recibido de la cola y cargarlo
        """
        queue = args[0]
        data = []
        await asyncio.sleep(1)
        try:
            #breakpoint()
            async for elem in read_async_queue(queue):
                # transformar elem para que sea guardable
                if isinstance(elem, dict):
                    try:
                        data_log = await statusdata2log(
                            elem.get("station"), **elem.get("data"))
                        if data_log:
                            try:
                                data.append(data_log)
                            except Exception as e:
                                bprint("Creando lista de logs, error %s, LogUnidadGNSS create" % e)
                                raise e
                    except Exception as e:
                        print("Error al transformar elem %s" % e)
            if data:
                #await dbaccess(LogUnidadGNSS.objects.bulk_create)(data)
                r = self.pool.map_async(data_save, data)
                r.wait()
        except Exception as e:
            print("Hubo una excepción al guardar los datos de LogGNSS")
            raise e
        data = []
        return args, kwargs

    def task_cycle(self):
        loop = asyncio.get_event_loop()
        tasks_list = []
        """
        RMQ Task
        """
        rmq_engine = {channel: RMQEngine(**value_dict)
                      for channel, value_dict in self.engine_opts.items()}
        {rmq.active_queue_switch() for rmq in rmq_engine.values()}
        # se crea el conjunto de canales existentes
        channels = set(self.engine_opts.keys())
        # mq 2 ws
        # la args de rmq
        # se activa ciclo de lectura rmq

        cycle_rmq_args = [rmq_engine, 0, channels]
        coroutine_future = coromask(self.cycle_read_from_rmq,
                                    cycle_rmq_args, {},
                                    simple_fargs_out)
        task = loop.create_task(coroutine_future)
        task.add_done_callback(
            fc.partial(renew, task, self.cycle_read_from_rmq, simple_fargs_out))
        # se agrega a lista de tareas:
        tasks_list.append(task)


        # se activa ciclo de escritura dj, leyendo cola async
        queue_dj = self.queue_set.get('status')
        cycle_dj_args = [queue_dj]
        coroutine_future = coromask(self.cycle_send_to_dj,
                                    cycle_dj_args,{},
                                    simple_fargs_out)
        task = loop.create_task(coroutine_future)
        task.add_done_callback(
            fc.partial(renew, task, self.cycle_send_to_dj, simple_fargs_out))
        # se agrega a lista de tareas:
        tasks_list.append(task)

        if not loop.is_running():
            loop.run_forever()
