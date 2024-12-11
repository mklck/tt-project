import socket

import keyExchange as ex
import crypto
import random
import select
import sys
import queue

#from .RSAConn	import RSAConn


class ServerTCP:
    BUFFER_SIZE = 20000
	
    def __init__(self):
        self.crypto = crypto.cryptographic(32)
        self.keyEx = ex.keyExchange(crypto);

    def bindServer(self, TCP_IP = '127.0.0.1', TCP_PORT = 5005):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('127.0.0.1', 5005))
        self.server.listen(5)

        self.inputs = [ self.server ]
        self.turn = 0;

    def randomizeOrder(self, s):
        if random.randint(0, 1) == 1:
            s.send(self.crypto.encrypt("SERVER_START".encode()));
            print("Serwer zaczyna");
            self.turn = 1;
        else:
            s.send(self.crypto.encrypt("CLIENT_START".encode()));
            print("Klient zaczyna");
            self.turn = 0;
 

    def runServer(self):
        # Wait for at least one of the sockets to be ready for processing
            readable, _, exceptional = select.select(self.inputs, [], self.inputs)

            for s in readable:

                if s is self.server:
                    # A "readable" server socket is ready to accept a connection
                    connection, client_address = s.accept()
                    print('new connection from', client_address);
                    
                    exchange = ex.keyExchange(self.crypto);
                    exchange.keyTransmissionServer(connection);

                    self.inputs.append(connection)
                    self.randomizeOrder(connection);
                    self.conn = connection;



    def serverSend(self,send_data: bytes):
            self.conn.send(self.crypto.encrypt(send_data));
            self.turn = 0;
            
    def serverRead(self):
            self.conn.settimeout(0.2)
            try:
                data = self.conn.recv(1024)
                print(self.crypto.decrypt(data).decode());
                self.turn = 1;
            except:
                pass
            self.conn.settimeout(None)
                    
 



            
