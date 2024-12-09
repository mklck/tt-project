import socket
import time
import game.crypto as crypto
from enum import Enum

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

class ClientTCP:
<<<<<<< HEAD
    
        def __init__(self):
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            self.crypto_client = crypto.cryptographic(32);
            self.conn = 0;
=======
	def __init__(self):
		self.crypto_client = crypto.cryptographic(32);
		self.conn = None
>>>>>>> 851b831185f6c1ad7b8f5466f4c7a9c940071e63

	def receive(self):
		try:
			data = self.s.recv(128)
			decrypted = self.crypto_client.decrypt(data)
			return decrypted
		except:
			print("Connection lost")
			self.s.close()

<<<<<<< HEAD
                                event.set();
                                board.put(received_board);
                        except:
                                print("Brak polaczenia");
                                self.s.close();
                                lock.release();
                                self.conn = 0;
                                return;
                
=======
>>>>>>> 851b831185f6c1ad7b8f5466f4c7a9c940071e63

	def send(self, data : bytes):
		try:
			encrypted = self.crypto_client.encrypt( data )
			self.s.send(encrypted)
		except:
			print("Connection lost");
			self.s.close();

<<<<<<< HEAD
                                # convert each item to int type
                                for i in range(len(board)):
                                        board[i] = int(board[i])
                                        
                                queue.get(); # just for remove
                                queue.put(board);
                                print("Wysłana plansza: ", *board );
                                data = bytes(board);

                                data_encrypted = self.crypto_client.encrypt( data );

                                try:
                                        self.s.send( data_encrypted );
                                        event.clear();
                                except:
                                        print("Brak polaczenia");
                                        self.s.close();
                                        lock.release();
                                        self.conn = 0;
                                        return;
                        else:
                                print("Oczekiwanie na ruch gracz (...) ");
                                time.sleep(0.5);

        def exit(self):
            self.s.close();        
=======
	def exit(self):
		self.s.close()
>>>>>>> 851b831185f6c1ad7b8f5466f4c7a9c940071e63
             
	def connect_serwer(self, TCP_IP = '127.0.0.1', TCP_PORT = 5005, BUFFER_SIZE = 20000):
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect((TCP_IP, TCP_PORT))
			print(f"Connected to {TCP_IP}:{TCP_PORT}")
		except:
			print("Could not connect to server")

		conn_state = Color.PUBLIC_KEY_EXCHANGE_SERVER

		while 1:
			match conn_state:
				case Color.PUBLIC_KEY_EXCHANGE_SERVER:
					data = self.s.recv(BUFFER_SIZE);
					if data.decode()[0:10] != "PUBLIC_KEY":
						continue
                            
					public_pair = data.decode()[10:].split();
					print("PUBLICE KEY GOT:", int(public_pair[0]) )
					self.crypto_client.RSA.key.exponent_sym = int(public_pair[0]);
					self.crypto_client.RSA.key.modulus_sym = int(public_pair[1]);
					self.s.send("KEY_ACK".encode());
					conn_state = Color.PUBLIC_KEY_EXCHANGE_CLIENT;

				case Color.PUBLIC_KEY_EXCHANGE_CLIENT:
					print("Sending public key [integer]: {} and modulus {}".format(
							self.crypto_client.RSA.key.exponent,
							self.crypto_client.RSA.key.modulus
						)
					)
					self.s.send(
						"PUBLIC_KEY".encode()
						+ (str(self.crypto_client.RSA.key.exponent)).encode()
						+ (" ").encode()
						+ (str(self.crypto_client.RSA.key.modulus)).encode()
					)
					conn_state = Color.SERVER_KEY_ACK;
                        
<<<<<<< HEAD
                    case Color.SERVER_KEY_ACK:
                         print("Waiting for publick key ACK from serwer")
                         data = self.s.recv(BUFFER_SIZE);
                         
                         if data.decode()[0:7] == "KEY_ACK":
                            print("ACK Got")
                            self.conn = 1;
                            return




=======
				case Color.SERVER_KEY_ACK:
					print("Waiting for publick key ACK from serwer")
					data = self.s.recv(BUFFER_SIZE);
					if data.decode()[0:7] == "KEY_ACK":
						print("ACK Got")
						return
>>>>>>> 851b831185f6c1ad7b8f5466f4c7a9c940071e63
