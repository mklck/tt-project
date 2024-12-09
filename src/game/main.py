import socket
import time
import crypto
from enum import Enum
from dataclasses	import dataclass
from _thread import *
import threading
import queue as q
import server_tcp



if __name__== "__main__":
    server = server_tcp.SerwerTCP();
    server.bind_serwer();

    event = threading.Event();
    
    conn, addr = server.s.accept()
    conn = server.connection(conn, event);
    print('Connection address:', addr)

    
    print_thread = threading.Lock();
    read_thread = threading.Lock();

    ### wspoldzielona plansza miedzy watkami, na poczatku pusta
    board = q.Queue();
    board.put([0,0,0,0,0,0,0,0,0])

    print_thread.acquire();
    start_new_thread(server.send, (conn,print_thread, event, board))
        
    read_thread.acquire();
    start_new_thread(server.receive, (conn,read_thread, event, board))
    
    while 1:
        pass

        
        

