from .serverTCP         import ServerTCP
from .gui		import Gui, GameQuit
from .circleCross	import CircleCross, FieldType
from .types		import Point

class Server:
	def __init__(self):
                self.gui = Gui(Point(800,800))
                self.s = ServerTCP()
                self.s.bindServer()
	def run(self):
                
                while True:
                        self.s.runServer();
                        
                        if self.s.turn == 0:
                                self.s.serverRead();
                                
                        if self.s.turn == 1 :
                                send_data = 'Cos do wyslania'
                                #self.s.serverSend(send_data.encode());
                                
                        self.tick(self.s.turn);
		
	def tick(self,turn):
		try:
			self.gui.tick(turn)
		except GameQuit:
			print('quit game')
			exit()
			
def server():
	Server().run()
