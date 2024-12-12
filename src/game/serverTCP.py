import socket

from .keyExchange import keyExchange as ex
from .crypto import cryptographic
import random
import select
import sys
import queue

#from .RSAConn	import RSAConn


class ServerTCP:
    BUFFER_SIZE = 20000
	
    def __init__(self):
        self.crypto = cryptographic(32)
        self.keyEx = ex(self.crypto);

    def bindServer(self, TCP_IP = '127.0.0.1', TCP_PORT = 5005):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('127.0.0.1', 5005))
        self.server.listen(5)
        self.server.setblocking(0)
        
        self.inputs = [ self.server ]
        self.turn = -1;

    def randomizeOrder(self, s):
        order_sign = '';
        
        if random.randint(0, 1) == 1:
            order_sign = "SERVER_START_"
            print("Serwer zaczyna");
            self.turn = 1;
        else:
            order_sign = "CLIENT_START_"
            print("Klient zaczyna");
            self.turn = 0;

        if random.randint(0, 1) == 1:
            self.sign = 'cross_'
            order_sign = order_sign + 'circle';
        else:
            self.sign = 'circle'
            order_sign = order_sign + 'cross_';

        s.send(self.crypto.encrypt(order_sign.encode()));
 

    def runServer(self):
        # Wait for at least one of the sockets to be ready for processing
            readable, _, exceptional = select.select(self.inputs, [], self.inputs, 1)
            #print("Waiting for new connection");
            for s in readable:

                if s is self.server:
                    # A "readable" server socket is ready to accept a connection
                    connection, client_address = s.accept()
                    print('new connection from', client_address);
                    connection.setblocking(1)
                    exchange = ex(self.crypto);
                    exchange.keyTransmissionServer(connection);
                    connection.setblocking(0)
                    self.inputs.append(connection)
                    self.randomizeOrder(connection);
                    self.conn = connection;
                    return 1;
            return 0;


    def serverSend(self,send_data: bytes):
            self.conn.send(self.crypto.encrypt(send_data));
            self.turn = 0;
            
    def serverRead(self):
            self.conn.settimeout(0.2)
            try:
                data = self.conn.recv(1024)
                #print(self.crypto.decrypt(data).decode());
                self.turn = 1;
            except:
                pass
            self.conn.settimeout(None)
                    
 



            
