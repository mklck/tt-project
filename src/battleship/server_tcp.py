import socket
import time
import crypto
from enum import Enum

## TCP/IP 
TCP_IP = '127.0.0.1' # Server address
TCP_PORT = 5005
BUFFER_SIZE = 20000  # Normally 1024, but we want fast response

## Maszyna stanów
class Color(Enum):
    PUBLIC_KEY_EXCHANGE = 1
    PUBLIC_KEY_ACK = 2
    COMMUNICATION = 3

Color = Enum('Color', [('PUBLIC_KEY_EXCHANGE', 1), ('PUBLIC_KEY_ACK', 2), ('COMMUNICATION', 3), ('END_CONN', 4)] )
conn_state = Color.PUBLIC_KEY_EXCHANGE;


## RSA+Padding Class
crypto = crypto.cryptographic(32);
print("Public key: ", str(crypto.RSA.key.modulus)); 

## Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)


################ CONNECTION ################################
conn, addr = s.accept()
print('Connection address:', addr)

while 1:
    #if not data: break
    match conn_state:
        case Color.PUBLIC_KEY_EXCHANGE:
             print("Sending public key [integer]:", crypto.RSA.key.exponent)
             conn.send("PUBLIC_KEY".encode() + (str(crypto.RSA.key.exponent)).encode() + (" ").encode() + (str(crypto.RSA.key.modulus)).encode() )
             conn_state = Color.PUBLIC_KEY_ACK;
        case Color.PUBLIC_KEY_ACK:
             print("Waiting for publick key ACK from client")
             data = conn.recv(BUFFER_SIZE);
             print(data.decode());
             if data.decode()[0:7] == "KEY_ACK":
                 conn_state = Color.COMMUNICATION;
        case Color.COMMUNICATION:
             try:
                 data = conn.recv(128);
                 print("Zaszyfrowana Wiadomosc: ");
                 print(data);
                 decrypted = crypto.decrypt(data);
                 print("Odszyfrowana Wiadomosc: " + decrypted.decode());
             except:
                 conn_state = Color.END_CONN;
        case Color.END_CONN:
             conn.close()
             print("End of communication")

             
    ## End of loop    
    time.sleep(1)
        
conn.close()
