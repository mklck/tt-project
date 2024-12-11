import socket
import crypto
import select

from enum	import Enum


Color = Enum(
	'Color',
	[
		('PUBLIC_KEY_EXCHANGE_SERVER', 1),
		('CLIENT_KEY_ACK', 2),
		('PUBLIC_KEY_EXCHANGE_CLIENT', 3),
		('SERVER_KEY_ACK', 4),
		('COMMUNICATION', 5),
		('END_CONN', 6)
	]
)

class keyExchange:

	def __init__(self, crypto):
		self.crypto = crypto
		self.BUFFER_SIZE = 20000;

	def keyTransmissionServer(self, conn):
		conn_state = Color.PUBLIC_KEY_EXCHANGE_SERVER

		while 1:
                    match conn_state:
                        case Color.PUBLIC_KEY_EXCHANGE_SERVER:
                                print("Sending public key [integer]: {} and modulus: {}".format(
                                        self.crypto.RSA.key.exponent, 
                                        self.crypto.RSA.key.modulus
                                        )
                                )
                                conn.send(
                                        "PUBLIC_KEY".encode()
                                        + (str(self.crypto.RSA.key.exponent)).encode()
                                        + (" ").encode()
                                        + (str(self.crypto.RSA.key.modulus)).encode()
                                )
                                conn_state = Color.CLIENT_KEY_ACK;
                     
                        case Color.CLIENT_KEY_ACK:
                                print("Waiting for publick key ACK from client")
                                data = conn.recv(self.BUFFER_SIZE);
                                print(data.decode());
                                if data.decode()[0:7] == "KEY_ACK":
                                        conn_state = Color.PUBLIC_KEY_EXCHANGE_CLIENT;

                        case Color.PUBLIC_KEY_EXCHANGE_CLIENT:
                                data = conn.recv(self.BUFFER_SIZE);
                                if data.decode()[0:10] == "PUBLIC_KEY":
                                        public_pair = data.decode()[10:].split();
                                        print("PUBLICE KEY GOT:", int(public_pair[0]) )
                                        self.crypto.RSA.key.exponent_sym = int(public_pair[0]);
                                        self.crypto.RSA.key.modulus_sym = int(public_pair[1]);
                                        conn.send("KEY_ACK".encode());
                                        return conn

	def keyTransmissionClient(self, conn):
		conn_state = Color.PUBLIC_KEY_EXCHANGE_SERVER

		while 1:
			match conn_state:
				case Color.PUBLIC_KEY_EXCHANGE_SERVER:
					data = conn.recv(self.BUFFER_SIZE);
					if data.decode()[0:10] != "PUBLIC_KEY":
						continue
                            
					public_pair = data.decode()[10:].split();
					print("PUBLICE KEY GOT:", int(public_pair[0]) )
					self.crypto.RSA.key.exponent_sym = int(public_pair[0]);
					self.crypto.RSA.key.modulus_sym = int(public_pair[1]);
					conn.send("KEY_ACK".encode());
					conn_state = Color.PUBLIC_KEY_EXCHANGE_CLIENT;

				case Color.PUBLIC_KEY_EXCHANGE_CLIENT:
					print("Sending public key [integer]: {} and modulus {}".format(
							self.crypto.RSA.key.exponent,
							self.crypto.RSA.key.modulus
						)
					)
					conn.send(
						"PUBLIC_KEY".encode()
						+ (str(self.crypto.RSA.key.exponent)).encode()
						+ (" ").encode()
						+ (str(self.crypto.RSA.key.modulus)).encode()
					)
					conn_state = Color.SERVER_KEY_ACK;
                        
				case Color.SERVER_KEY_ACK:
					print("Waiting for publick key ACK from serwer")
					data = conn.recv(self.BUFFER_SIZE);
					if data.decode()[0:7] == "KEY_ACK":
						print("ACK Got")
						return
