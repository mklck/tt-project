import socket
import time
import crypto
from enum import Enum
from dataclasses	import dataclass

## Maszyna stanów
class Color(Enum):
    PUBLIC_KEY_EXCHANGE = 1
    PUBLIC_KEY_ACK = 2
    COMMUNICATION = 3

Color = Enum('Color', [('PUBLIC_KEY_EXCHANGE_SERVER', 1), ('CLIENT_KEY_ACK', 2), ('PUBLIC_KEY_EXCHANGE_CLIENT', 3), ('SERVER_KEY_ACK', 4), ('COMMUNICATION', 5) , ('END_CONN', 6)] )
    
@dataclass
class SerwerTCP:
	
        def __init__(self):
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            self.crypto = crypto.cryptographic(32);
            self.conn = None

        def receive(self):
            try:
                data = self.conn.recv(128);
                print("Zaszyfrowana Wiadomosc: ");
                print(data);
                decrypted = self.crypto.decrypt(data);
                print("Odszyfrowana Wiadomosc: " + decrypted.decode());
            except:
                print("Brak polaczenia");

        def send(self):
            msg = input('Wpisz wiadomosc: ');
            data = msg.encode();
            
            data_encrypted = self.crypto.encrypt( msg.encode() );
            
            try:
                self.conn.send( data_encrypted );
            except:
                print("Brak polaczenia");
                self.bind_serwer();
 

            

        def bind_serwer(self, TCP_IP = '127.0.0.1', TCP_PORT = 5005, BUFFER_SIZE = 20000):
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                self.s.bind((TCP_IP, TCP_PORT))
                self.s.listen(1)

                conn_state = Color.PUBLIC_KEY_EXCHANGE_SERVER;
                self.conn, addr = self.s.accept()
                print('Connection address:', addr)
                
                while 1:
                    match conn_state:
                        case Color.PUBLIC_KEY_EXCHANGE_SERVER:
                            
                             print("Sending public key [integer]:", self.crypto.RSA.key.exponent, "and modulus: ", self.crypto.RSA.key.modulus)
                             self.conn.send("PUBLIC_KEY".encode() + (str(self.crypto.RSA.key.exponent)).encode() + (" ").encode() + (str(self.crypto.RSA.key.modulus)).encode() )
                             conn_state = Color.CLIENT_KEY_ACK;
                             
                        case Color.CLIENT_KEY_ACK:
                             print("Waiting for publick key ACK from client")
                             data = self.conn.recv(BUFFER_SIZE);
                             print(data.decode());
                             if data.decode()[0:7] == "KEY_ACK":
                                 conn_state = Color.PUBLIC_KEY_EXCHANGE_CLIENT;

                        case Color.PUBLIC_KEY_EXCHANGE_CLIENT:
                            data = self.conn.recv(BUFFER_SIZE);
                            if data.decode()[0:10] == "PUBLIC_KEY":
                                public_pair = data.decode()[10:].split();
                                print("PUBLICE KEY GOT:", int(public_pair[0]) )
                                self.crypto.RSA.key.exponent_sym = int(public_pair[0]);
                                self.crypto.RSA.key.modulus_sym = int(public_pair[1]);
                                self.conn.send("KEY_ACK".encode());
                                
                                return


    



