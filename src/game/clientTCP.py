import socket
import time
import crypto
import queue as q
import keyExchange as ex

class ClientTCP:
    BUFFER_SIZE = 20000
	
    def __init__(self):
        self.crypto = crypto.cryptographic(32);
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.turn = 0;
        
    def connectServer(self, TCP_IP = '127.0.0.1', TCP_PORT = 5005):
        self.sock.connect(('127.0.0.1', 5005));
        self.exchange = ex.keyExchange(self.crypto);
        self.exchange.keyTransmissionClient(self.sock);
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow for polling
 
    def clientRead(self):
        self.sock.settimeout(0.2)
        
        try:
            data = self.sock.recv(1024);
            data = self.crypto.decrypt(data);
            if data.decode()[-12:] == "CLIENT_START":
                print("Klient zaczyna");
                self.turn = 1;
            elif data.decode()[-12:] == "SERVER_START":
                print("Serwer zaczyna");
                self.turn = 0;
            elif len(data.decode()) > 0:
                print(data.decode());
                self.turn = 1;
                
        except:
            pass
        
        self.sock.settimeout(None)

    def clientSend(self, send_data: bytes):
            self.sock.send(self.crypto.encrypt(send_data));
            self.turn = 0;
            

