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
                                break;
                        self.tick(self.tcp.turn);
                        
                while  self.tcp.sign == None:
                        self.tcp.clientRead();
                        self.tick(self.tcp.turn);

                    
                print("Gui ustawione");   
                self.gui.setSign(self.tcp.sign);
                
                while True:
                        
                        if self.tcp.turn == 0 or self.tcp.turn == -1:
                                self.tcp.clientRead();
                                
                        if self.tcp.turn == 1 and  self.gui.game.move_done == 1:
                                send_data = 'Cos do wyslania'
                                self.tcp.clientSend(send_data.encode());
                                self.gui.game.move_done = 0;
                               
                        self.tick(self.tcp.turn);
                        
	def tick(self,turn):
		try:
			self.gui.tick(turn)
		except GameQuit:
			print('quit game')
			exit()
