from tasktools.taskloop import coromask, renew, simple_fargs, simple_fargs_out
import asyncio
import websockets as ws
import functools as fc
from networktools.time import timestamp
from networktools.library import my_random_string
from networktools.colorprint import gprint, bprint, rprint
import ujson as json


def generate_data(*args, **kwargs):
    return {'text': my_random_string(), 'time': timestamp()}


class WSServer:
    def __init__(self, *args, **kwargs):
        self.__status = False
        self.__host = kwargs.get('host', 'localhost')
        self.__port = kwargs.get('port', 6776)
        self.__delta_time = kwargs.get('delta_time', 1)
        self.__genfun = kwargs.get('genfun', generate_data)

    async def data_generator(self, websocket, path):
        while True:
            df_args = []
            df_kwargs = {}
            new_data = self.__genfun(*df_args, **df_kwargs)
            try:
                gprint("===NEW DATA===")
                rprint(new_data)
                rprint("====")
                await websocket.send(json.dumps(new_data))
            except Exception as e:
                bprint("====ERROR on SEND===")
                print("The exception is -> %s" % e)
                raise e
            try:
                bprint("WS recv...")
                #msg_recv = await websocket.recv()
                gprint("===NEW DATA ON SERVER===")
                #gprint(msg_recv)
                rprint("====")
            except Exception as e:
                bprint("====ERROR on RECV===")
                print("The exception is -> %s" % e)
                raise e
            rprint("Sleep %s" % self.__delta_time)
            await asyncio.sleep(self.__delta_time)

    def cycle(self):
        loop = asyncio.get_event_loop()
        server = ws.serve(self.data_generator, self.__host, self.__port)
        if not loop.is_running():
            loop.run_until_complete(server)
            loop.run_forever()


if __name__ == "__main__":
    kwargs = {'delta_time': .5, 'port': 8000, 'host':'10.54.218.13'}
    wsserver = WSServer(**kwargs)
    wsserver.cycle()
