import socket
import time
import crypto
from enum import Enum
from dataclasses	import dataclass

Color = Enum('Color', [('PUBLIC_KEY_EXCHANGE_SERVER', 1), ('CLIENT_KEY_ACK', 2), ('PUBLIC_KEY_EXCHANGE_CLIENT', 3), ('SERVER_KEY_ACK', 4), ('COMMUNICATION', 5) , ('END_CONN', 6)] )
conn_state = Color.PUBLIC_KEY_EXCHANGE_SERVER;

@dataclass
class ClientTCP:
    
        def __init__(self):
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            self.crypto_client = crypto.cryptographic(32);
            self.conn = None

        def receive(self, lock, token):
                while True:
                        try:
                                data = self.s.recv(128);
                                
                                decrypted = self.crypto_client.decrypt(data);
                                print("Odebrane: " + decrypted.decode());

                                token = 1;
                        except:
                                print("Brak polaczenia");
                                self.s.close();
                                lock.released();
                                return;
                

        def send(self, lock, token):
                 while True:
                        if token == 1:     
                                msg = input('Wpisz wiadomosc: ');
                                data = msg.encode();

                                data_encrypted = self.crypto_client.encrypt( msg.encode() );

                                try:
                                        self.s.send( data_encrypted );
                                        token = 0;
                                except:
                                        print("Brak polaczenia");
                                        self.s.close();
                                        lock.released();
                                return;
                        else:
                                print("Oczekiwanie na ruch gracz (...) ");
                                time.sleep(0.5);

        def exit(self):
            self.s.close();        
             
        def connect_serwer(self, TCP_IP = '127.0.0.1', TCP_PORT = 5005, BUFFER_SIZE = 20000):
            ##TCP_IP = name = input('Podaj IP serwera')

            connection = 1;
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            while connection:
                try:
                    self.s.connect((TCP_IP, TCP_PORT))
                    print("Nawiazano polaczenie");
                    connection = 0;
                except:
                    print("Brak odpowiedzi");

            conn_state = Color.PUBLIC_KEY_EXCHANGE_SERVER;

            while 1:
                match conn_state:
                    
                    case Color.PUBLIC_KEY_EXCHANGE_SERVER:
                        data = self.s.recv(BUFFER_SIZE);
                        if data.decode()[0:10] == "PUBLIC_KEY":
                            
                            public_pair = data.decode()[10:].split();
                            print("PUBLICE KEY GOT:", int(public_pair[0]) )
                            self.crypto_client.RSA.key.exponent_sym = int(public_pair[0]);
                            self.crypto_client.RSA.key.modulus_sym = int(public_pair[1]);
                            self.s.send("KEY_ACK".encode());
                            
                            conn_state = Color.PUBLIC_KEY_EXCHANGE_CLIENT;
                            
                    case Color.PUBLIC_KEY_EXCHANGE_CLIENT:
                        print("Sending public key [integer]:", self.crypto_client.RSA.key.exponent, "and modulus: ", self.crypto_client.RSA.key.modulus)
                        self.s.send("PUBLIC_KEY".encode() + (str(self.crypto_client.RSA.key.exponent)).encode() + (" ").encode() + (str(self.crypto_client.RSA.key.modulus)).encode() )
                            
                        conn_state = Color.SERVER_KEY_ACK;
                        
                    case Color.SERVER_KEY_ACK:
                         print("Waiting for publick key ACK from serwer")
                         data = self.s.recv(BUFFER_SIZE);
                         
                         if data.decode()[0:7] == "KEY_ACK":
                            print("ACK Got")
                            return




