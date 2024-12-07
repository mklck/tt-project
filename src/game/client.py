import socket
import time
import crypto
from enum import Enum
from dataclasses	import dataclass
import client_tcp


if __name__== "__main__":
    client = client_tcp.ClientTCP();
    client.connect_serwer();

    while 1:
        client.receive();
