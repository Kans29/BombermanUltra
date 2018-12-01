import pygame
from boton import Boton


class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
        
    def update(self):
        self.left,self.top = pygame.mouse.get_pos()

def menuInicial():
	winW,winH = 600,600
	myfont = pygame.font.SysFont('Comic Sans MS', 30)
	window = pygame.display.set_mode((winW,winH))
	pygame.display.set_caption("Bomberman Ultra")
	logo = pygame.image.load("Logo.png").convert_alpha()
	boton1a = pygame.image.load("boton1a.png").convert_alpha()
	boton1b = pygame.image.load("boton1b.png").convert_alpha()
	boton2a = pygame.image.load("boton2a.png").convert_alpha()
	boton2b = pygame.image.load("boton2b.png").convert_alpha()
	Word = myfont.render("Elija una dificultad:", False, (0,0,0))
	seleccion,exit = 0,0
	Cursor1 = Cursor()
	Boton1 = Boton(boton1a,boton1b,120,400)
	Boton2 = Boton(boton2a,boton2b,400,400)
	while seleccion == 0 and exit == 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = 1
			if(event.type == pygame.MOUSEBUTTONDOWN):
				if (Cursor1.colliderect(Boton1.rect)):
					seleccion = 1
				if (Cursor1.colliderect(Boton2.rect)):
					seleccion = 2
		pygame.Surface.fill(window,(255,255,255))
		window.blit(logo, pygame.rect.Rect(40,0, 128, 128))
		window.blit(Word,(170,300))
		Boton1.update(window,Cursor1)
		Boton2.update(window,Cursor1)
		Cursor1.update()
		#Boton1.update(window,Cursor1)
		pygame.display.update()

	pygame.display.quit()
	return seleccion