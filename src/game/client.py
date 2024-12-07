import socket
import time
import crypto
from enum import Enum
from dataclasses	import dataclass
from _thread import *
import threading
import client_tcp


if __name__== "__main__":
    client = client_tcp.ClientTCP();
    client.connect_serwer();

    print_thread = threading.Lock();
    read_thread = threading.Lock();

    token = 0;
    while 1:
        
        print_thread.acquire();
        start_new_thread(client.send, (print_thread, token))
        
        read_thread.acquire();
        start_new_thread(client.receive, (read_thread, token))
        
        #client.receive();
