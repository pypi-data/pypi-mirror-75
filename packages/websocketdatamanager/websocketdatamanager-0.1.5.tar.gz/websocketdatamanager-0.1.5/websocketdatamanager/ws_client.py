import asyncio
import websockets as ws
import functools as fc
from tasktools.taskloop import coromask, renew, simple_fargs, simple_fargs_out
from networktools.time import timestamp
from networktools.library import my_random_string
from networktools.colorprint import gprint, bprint, rprint
import ujson as json


def generate_data(*args, **kwargs):
    return {'text': my_random_string(), 'time': timestamp()}


class WSClient:
    def __init__(self, *args, **kwargs):
        self.__status = False
        self.__host = kwargs.get('host', 'localhost')
        self.__port = kwargs.get('port', 6776)
        self.__path = kwargs.get('path', None)
        self.__scheme = kwargs.get("scheme","ws")
        self.__delta_time = kwargs.get('delta_time', 1)
        self.__genfun = kwargs.get('genfun', generate_data)
        self.__ws_object = None
        self.__ping_freq = kwargs.get('heartbeat', 10)

    async def heartbeat(self, *args):
        uri = args[0]
        v = args[1]
        if v == 0:
            try:
                websocket = self.__ws_object
                if not websocket:
                    websocket = await ws.connect(uri)
                    self.__ws_object = websocket
                v += 1
                await asyncio.sleep(self.__delta_time)
                return uri, v, websocket
            except Exception as e:
                print("Exception on heartbeat connect %s" % e)
                v = 0
                websocket = None
                await asyncio.sleep(1)
                return uri, v, websocket
        else:
            websocket = args[2]
            try:
                pong_waiter = await websocket.ping()
                await pong_waiter
            except Exception as e:
                print("Exception on heartbeat %s" % e)
                v = 0
                websocket = None
                await asyncio.sleep(10)
                return uri, v, websocket
            await asyncio.sleep(self.__ping_freq)
            return uri, v, websocket

    def cycle_heartbeat(self, ws_args):
        loop = asyncio.get_event_loop()
        coroutine_future = coromask(self.heartbeat,
                                    ws_args,
                                    simple_fargs_out)
        ws_task = loop.create_task(coroutine_future)
        ws_task.add_done_callback(
            fc.partial(renew, ws_task,
                       self.heartbeat,
                       simple_fargs_out))
        return ws_task

    async def read_ws(self, *args):
        uri = args[0]
        v = args[1]
        if v == 0:
            try:
                print(uri, v)
                websocket = self.__ws_object
                if not websocket:
                    websocket = await ws.connect(uri)
                    self.__ws_object = websocket
                v += 1
                await asyncio.sleep(self.__delta_time)
                return uri, v, websocket
            except Exception as e:
                print("Exception on read_ws connect %s" % e)
                v = 0
                websocket = None
                await asyncio.sleep(1)
                return uri, v, websocket
        elif v == 1:
            websocket = args[2]
            try:
                data_recv = await websocket.recv()
            except Exception as e:
                rprint("Exception Timestamp %s" % timestamp())
                print("Exception on send msg, %s" % e)
                v = 0
                self.__ws_object = None
                await asyncio.sleep(1)
                return uri, v, websocket
            await asyncio.sleep(self.__delta_time)
            return uri, v, websocket

    async def send_ws(self, *args):
        """
        To implent....
        """
        uri = args[0]
        v = args[1]
        if v == 0:
            try:
                websocket = self.__ws_object
                if not websocket:
                    websocket = await ws.connect(uri)
                    self.__ws_object = websocket
                v += 1
                await asyncio.sleep(self.__delta_time)
                return uri, v, websocket
            except Exception as e:
                print("Exception on send_ws connect %s" % e)
                v = 0
                websocket = None
                await asyncio.sleep(1)
                return uri, v, websocket
        elif v == 1:
            websocket = args[2]
            df_args = []
            df_kwargs = {}
            new_data = self.__genfun(*df_args,
                                     **df_kwargs)
            rprint("== DATA SEND ==")
            bprint(new_data)
            msg = {'message': new_data, 'destiny': 'ws_users'}
            try:
                await websocket.send(json.dumps(msg))
            except Exception as e:
                rprint("Exception Timestamp %s" % timestamp())
                print("Exception on send msg, %s" % e)
                v = 0
                self.__ws_object = None
                await asyncio.sleep(1)
                return uri, v, websocket

            await asyncio.sleep(self.__delta_time)
            return uri, v, websocket

    async def cycle_read_from_queue(self, *args):
        uri = args[0]
        v = args[1]
        queue = args[3]
        if v == 0:
            websocket = self.__ws_object
            if not websocket:
                websocket = await ws.connect(uri)
                self.__ws_object = websocket
            v += 1
            await asyncio.sleep(self.__delta_time)
            return uri, v, websocket, queue
        elif v == 1:
            rprint("read from queue")
            websocket = args[2]
            if not queue.empty():
                for i in range(queue.qsize()):
                    msg = queue.get()
                    bprint("===MSG from RMQ===")
                    gprint(msg)
                    if type(msg) == dict:
                        # get channel from msg, to direct the msg
                        gprint("Sending to websocket")
                        msg_send = {'message': msg, 'destiny': 'ws_users'}
                        try:
                            await websocket.send(json.dumps(msg_send))
                        except Exception as e:
                            bprint("Error en read frm queue")
                            rprint("Exception Timestamp %s" % timestamp())
                            print("Exception on send msg, %s" % e)
                            v = 0
                            self.__ws_object = None
                            return uri, v, websocket, queue
                    queue.task_done()
            await asyncio.sleep(self.__delta_time)
            return uri, v, websocket, queue

    async def cycle_send_to_queue(self, *args):
        uri = args[0]
        v = args[1]
        queue = args[3]
        if v == 0:
            print(uri, v)
            websocket = self.__ws_object
            if not websocket:
                websocket = await ws.connect(uri)
                self.__ws_object = websocket
            v += 1
            await asyncio.sleep(self.__delta_time)
            return uri, v, websocket, queue
        elif v == 1:
            websocket = args[2]
            try:
                data_recv = await websocket.recv()
                rprint("== DATA RECV ==")
                bprint(json.loads(data_recv))
                queue.put(json.loads(data_recv))
            except Exception as e:
                rprint("Exception Timestamp %s" % timestamp())
                print("Exception on send msg, %s" % e)
                v = 0
                self.__ws_object = None
            await asyncio.sleep(self.__delta_time)
            return uri, v, websocket, queue

    def build_uri(self):
        scheme =  self.__scheme
        host = self.__host
        path = self.__path
        port = 8000
        if host != 'localhost':
            port = self.__port
        uri = ''

        if scheme == "wss":
            if not self.__path:
                uri = f"wss://{host}"
            else:
                uri = f"wss://{host}/{path}"
        else:
            if not self.__path:
                uri = f"ws://{host}:{port}"
            else:
                uri = f"ws://{host}:{port}/{path}"
        return uri

    def get_args(self):
        uri = self.build_uri()
        rprint("Get args...")
        return [uri, 0, None]

    def cycle(self):
        loop = asyncio.get_event_loop()
        args = self.get_args()
        coroutine_future = coromask(
            self.read_ws, args, simple_fargs_out)
        task = loop.create_task(coroutine_future)
        task.add_done_callback(
            fc.partial(renew, task, self.read_ws, simple_fargs_out))
        # recv_coro
        if not loop.is_running():
            loop.run_until_complete(task)
            loop.run_forever()

    def cycle_send(self):
        loop = asyncio.get_event_loop()
        args = self.get_args()
        coroutine_future = coromask(
            self.send_ws, args, simple_fargs_out)
        task = loop.create_task(coroutine_future)
        task.add_done_callback(
            fc.partial(renew, task,
                       self.send_ws,
                       simple_fargs_out))
        recv_coroutine_future = coromask(
            self.read_ws, args, simple_fargs_out)
        recv_task = loop.create_task(
            recv_coroutine_future)
        recv_task.add_done_callback(
            fc.partial(renew, recv_task,
                       self.read_ws,
                       simple_fargs_out))
        if not loop.is_running():
            loop.run_until_complete(task)
            loop.run_forever()


if __name__ == "__main__":
    kwargs = {'delta_time': .5, 'port': 9012}
    wsserver = WSClient(**kwargs)
    wsserver.cycle()
