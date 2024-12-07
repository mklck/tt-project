import socket
import time
import crypto
from enum import Enum
from dataclasses	import dataclass
from _thread import *
import threading
import server_tcp



if __name__== "__main__":
    server = server_tcp.SerwerTCP();
    server.bind_serwer();
    
    print_thread = threading.Lock();
    read_thread = threading.Lock();
    
    while 1:
        conn, addr = server.s.accept()
        server.connection(conn);
        
        print_thread.acquire();
        start_new_thread(server.send, (conn,print_thread))
        
        read_thread.acquire();
        start_new_thread(server.receive, (conn,read_thread))
        
        #server.send(conn);
