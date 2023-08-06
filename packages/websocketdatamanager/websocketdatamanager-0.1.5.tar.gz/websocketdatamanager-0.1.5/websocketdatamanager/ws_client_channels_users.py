from ws_client import WSClient

if __name__ == "__main__":
    kwargs = {
        'delta_time': .5,
        'port': 8000,
        'path': 'ws/status_all/ws_users/'}
    wsserver = WSClient(**kwargs)
    wsserver.cycle()
