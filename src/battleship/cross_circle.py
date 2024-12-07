import pygame, sys, math

pygame.init()

WIDTH = 800;
HEIGHT = 800;
BACKGROUND_COLOR = (00,102,51);
LINE_COLOR = (255,128,0);

screen = pygame.display.set_mode((WIDTH,HEIGHT));
pygame.display.set_caption("Kółko i krzyżyk");
screen.fill( BACKGROUND_COLOR )

pygame.draw.line( screen, LINE_COLOR, (100,100) , (100,700), 10 );
pygame.draw.line( screen, LINE_COLOR, (300,100) , (300,700), 10 );
pygame.draw.line( screen, LINE_COLOR, (500,100) , (500,700), 10 );
pygame.draw.line( screen, LINE_COLOR, (700,100) , (700,700), 10 );

pygame.draw.line( screen, LINE_COLOR, (100,100) , (700,100), 10 );
pygame.draw.line( screen, LINE_COLOR, (100,300) , (700,300), 10 );
pygame.draw.line( screen, LINE_COLOR, (100,500) , (700,500), 10 );
pygame.draw.line( screen, LINE_COLOR, (100,700) , (700,700), 10 );


#MAIN LOOP
while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit();

        pygame.display.update()
