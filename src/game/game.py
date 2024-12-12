from .clientTCP	        import ClientTCP
from .gui		import Gui, GameQuit
from .circleCross	import CircleCross, FieldType
from .types		import Point

class Game:
	def __init__(self):
		self.gui = Gui(Point(800,800))
		self.tcp = ClientTCP()
		
	def run(self):

                while True:
                        if self.tcp.connectServer() == 1:
                                continue;
                        self.tick();

                while True:
                        if self.tcp.turn == 0:
                                self.s.serverRead();
                                
                        if self.tcp.turn == 1:
                               self.s.serverSend(send_data.encode());
                               
                        self.tick();
                        
	def tick(self):
		try:
			self.gui.tick()
		except GameQuit:
			print('quit game')
			exit()
