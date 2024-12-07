import socket
import time
import crypto
from enum import Enum
from dataclasses	import dataclass
import server_tcp
import client_tcp


if __name__== "__main__":
    server = server_tcp.SerwerTCP();
    server.bind_serwer();
    
    while 1:
        server.send();

        
