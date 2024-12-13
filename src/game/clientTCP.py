import socket
import time
from .crypto import cryptographic
import queue as q
from .keyExchange import keyExchange as ex

class ClientTCP:
    BUFFER_SIZE = 20000
	
    def __init__(self):
        self.crypto = cryptographic(32);
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow for polling
        self.turn = -1;
        self.sign = None;
        
    def connectServer(self, TCP_IP = '127.0.0.1', TCP_PORT = 5005):
        self.sock.settimeout(0.05)
        
        try:
            
            self.sock.connect(('127.0.0.1', 5005));
            self.sock.settimeout(None)
            print("Wchodzi1");
            self.exchange = ex(self.crypto);
 
            self.exchange.keyTransmissionClient(self.sock);
            return 1
        except:
            pass;
            return 0;
        self.sock.settimeout(None)
         
    def clientRead(self):
        self.sock.settimeout(0.05)
        
        try:
            data = self.sock.recv(1024);
            data = self.crypto.decrypt(data);

            if data.decode()[-19:-7] == "CLIENT_START":
                    print("Klient zaczyna");
                    self.turn = 1;
            elif data.decode()[-19:-7] == "SERVER_START":
                    print("Serwer zaczyna");
                    self.turn = 0;
            elif len(data.decode()) > 0:
                    self.turn = 1;
    
            if data.decode()[-6:] == "cross_":
                    print("Masz krzyzyk");
                    self.sign = 'cross_'
            elif data.decode()[-6:] == "circle":
                    print("Masz kolko");
                    self.sign = 'circle'

            self.sock.settimeout(None)
            return data;
            
        except:
            pass
        
        self.sock.settimeout(None)
        
        

    def clientSend(self, send_data: bytes):
            self.sock.send(self.crypto.encrypt(send_data));
            self.turn = 0;
