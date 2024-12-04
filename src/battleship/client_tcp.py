import socket
import time
import crypto
from enum import Enum

## TCP/IP 
TCP_PORT = 5005
BUFFER_SIZE = 20000
TCP_IP = '127.0.0.1' # Server address
##TCP_IP = name = input('Podaj IP serwera')

## Maszyna stanów
class Color(Enum):
    PUBLIC_KEY_EXCHANGE = 1
    PUBLIC_KEY_ACK = 2
    COMMUNICATION = 3

Color = Enum('Color', [('PUBLIC_KEY_EXCHANGE', 1), ('PUBLIC_KEY_ACK', 2), ('COMMUNICATION', 3), ('END_CONN', 4)] )
conn_state = Color.PUBLIC_KEY_EXCHANGE;

## RSA+Padding Class
crypto_client = crypto.cryptographic(32);

 
## Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


################ CONNECTION ################################
while 1:
    match conn_state:
        case Color.PUBLIC_KEY_EXCHANGE:
            data = s.recv(BUFFER_SIZE);
            if data.decode()[0:10] == "PUBLIC_KEY":
                
                public_pair = data.decode()[10:].split();
                print("PUBLICE KEY GOT:", int(public_pair[0]) )
                crypto_client.RSA.key.exponent = int(public_pair[0]);
                crypto_client.RSA.key.modulus = int(public_pair[1]);
                s.send("KEY_ACK".encode());
                conn_state = Color.COMMUNICATION;
        case Color.COMMUNICATION:
            msg = input('Wpisz wiadomosc: ');
            try:
                s.send(crypto_client.encrypt( msg.encode() ));
            except:
                conn_state = Color.END_CONN;
        case Color.END_CONN:
            s.close()
            print("End of communication")

    ## End of loop
    time.sleep(1)
    
s.close();
