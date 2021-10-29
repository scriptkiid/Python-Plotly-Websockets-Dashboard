from websocket import create_connection
from pprint import pprint
from time import time


if __name__ == '__main__':
    ws = create_connection(f'ws://127.0.0.1:5000/data')
    count = 0
    start = time()
    while True:
        pprint(ws.recv())
        count += 1
        end = time()
        print(f'{count/(end-start):.2f} hz')
