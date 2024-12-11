import socket
import time
from enum import Enum
from dataclasses	import dataclass
from _thread import *
import threading
import queue as q


if __name__== "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 5005))
    sock.setblocking(0)

    while 1:
        data = 'foobar\n' * 10  * 1024  # 70 MB of data
        sock.send(data.encode())
        print("dziala");
        time.sleep(2);
