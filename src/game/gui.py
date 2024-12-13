import pygame as pg

from .types		import Point
from .circleCross	import CircleCross, FieldType, BoardPoint, FieldNotEmpty

class GameQuit(Exception):
	pass

class Gui:
        
        LINE_COLOR = (255,128,0);
        def __init__(self, res : Point ):
                pg.init()
                self.res = res
                self.screen = pg.display.set_mode((res.x, res.y))
                self.clock = pg.time.Clock()
                self.fill = 'black'
                self.thickness = 5
                self.font = pg.font.SysFont('Arial', 48)
                self.game = None;
        def setSign(self, sign):
                self.game = CircleCross(sign);
                
        def tick(self, turn):
                for e in pg.event.get():
                        if e.type == pg.QUIT:
                                raise GameQuit()
                        if e.type == pg.MOUSEBUTTONUP and turn == 1:
                                self.handleMouse(*e.pos,turn)
                self.screen.fill( (00,102,51) )
                self.drawBoard(turn)
                pg.display.flip()
                self.clock.tick(30)

        def handleMouse(self, x, y, turn):
                r = range(100, 701)
                if x not in r or y not in r:
                        return
                x = (x - 100) // 200
                y = (y - 100) // 200
                bp = BoardPoint(x=x, y=y)
                try:
                        self.game.hit(bp, turn)
                except FieldNotEmpty:
                        pass

        def drawRect(self, start : Point, end : Point):

                pg.draw.line( self.screen, (255,128,0), (100,100) , (100,700), 7 );
                pg.draw.line( self.screen, (255,128,0), (300,100) , (300,700), 7 );
                pg.draw.line( self.screen, (255,128,0), (500,100) , (500,700), 7 );
                pg.draw.line( self.screen, (255,128,0), (700,100) , (700,700), 7 );

                pg.draw.line( self.screen, (255,128,0), (100,100) , (700,100), 7 );
                pg.draw.line( self.screen, (255,128,0), (100,300) , (700,300), 7 );
                pg.draw.line( self.screen, (255,128,0), (100,500) , (700,500), 7 );
                pg.draw.line( self.screen, (255,128,0), (100,700) , (700,700), 7 );

        def drawBoard(self, turn):
                self.drawRect(Point(100, 100), Point(600, 600))
                if self.game:
                    self.drawFields()
                self.drawStatus(turn)

        def drawFields(self):
                for f in self.game.fields:
                        if f.type is FieldType.cross:
                                self.drawCross(f.pos)
                        elif f.type is FieldType.circle:
                                self.drawCircle(f.pos)

        def drawCross(self, bp : BoardPoint):
                x0 = 200 * bp.x + 150
                y0 = 200 * bp.y + 150

                x1 = 200 * bp.x + 225
                y1 = 200 * bp.y + 225

                x0, x1 = min(x0, x1), max(x0, x1)
                y0, y1 = min(y0, y1), max(y0, y1)

                self.drawLine(Point(x0, y0), Point(x1, y1))
                self.drawLine(Point(x0, y1), Point(x1, y0))

        def drawLine(self, start : Point, end : Point):
                pg.draw.line(
                        self.screen,
                        self.fill,
                        start.asTuple(),
                        end.asTuple(),
                        self.thickness
                )

        def drawCircle(self, bp : BoardPoint):
                x = 200 * bp.x + 200
                y = 200 * bp.y + 200
                pg.draw.circle(
                        self.screen,
                        self.fill,
                        (x, y),
                        50,
                        self.thickness
                )
        def drawStatus(self, turn):
                if turn == -1:      
                        fmt = 'Oczekiwanie na drugiego gracza'
                elif turn == 0:
                        fmt = 'Ruch przeciwnika'
                elif turn == 1:
                        fmt = 'Twój ruch'
                elif turn == 2:
                        fmt = 'Wygrały kółka'
                elif turn == 3:
                        fmt = 'Wygrały krzyżyki'
                else:
                        pass
                surface = self.font.render(fmt, True, self.fill)
                rect = surface.get_rect(center=(self.res.x // 2, 50))
                self.screen.blit(surface, rect)
