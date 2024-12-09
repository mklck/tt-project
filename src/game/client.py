import socket
import time
import crypto
from enum import Enum
from dataclasses	import dataclass
from _thread import *
import threading
import queue as q
import client_tcp


if __name__== "__main__":
    client = client_tcp.ClientTCP();
    client.connect_serwer();

    print_thread = threading.Lock();
    read_thread = threading.Lock();

    ### event blokuje/odblokowywuje ruch; send czysci, receive ustawia
    event = threading.Event();
    event.clear();
    
    ### wspoldzielone dane miedzy watkami 
    board = q.Queue();
    ### czysta plansza 
    board.put([0,0,0,0,0,0,0,0,0])

    ### watek do wysylania
    print_thread.acquire();
    start_new_thread(client.send, (print_thread, event, board))

    ### watek do czytania
    read_thread.acquire();
    start_new_thread(client.receive, (read_thread, event, board))

    
    while 1:
        pass
