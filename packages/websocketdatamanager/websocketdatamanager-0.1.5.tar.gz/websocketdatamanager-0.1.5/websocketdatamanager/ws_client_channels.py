from ws_client import WSClient

if __name__ == "__main__":
    kwargs = {
        'delta_time': 2,
        'port': 8000,
        'path': 'ws/status_all/ws_source/'}
    wsserver = WSClient(**kwargs)
    wsserver.cycle_send()
