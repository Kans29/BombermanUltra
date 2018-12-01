import pygame
from boton import Boton
from menu import Cursor

def menuPerdida():
	winW,winH = 821,461

	window = pygame.display.set_mode((winW,winH))
	pygame.display.set_caption("Bomberman Ultra")
	continuar1 = pygame.image.load("Continuar1.png").convert_alpha()
	continuar2 = pygame.image.load("Continuar2.png").convert_alpha()
	salir1 = pygame.image.load("Exit1.png").convert_alpha()
	salir2 = pygame.image.load("Exit2.png").convert_alpha()
	fin = pygame.image.load("fin.png").convert_alpha()
	seleccion,exit = 0,0
	Cursor1 = Cursor()
	Boton1 = Boton(continuar1,continuar2,413,177)
	Boton2 = Boton(salir1,salir2,463,290)
	while seleccion == 0 and exit == 0:
		window.blit(fin,(0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = 1
			if(event.type == pygame.MOUSEBUTTONDOWN):
				if (Cursor1.colliderect(Boton1.rect)):
					seleccion = 1
				if (Cursor1.colliderect(Boton2.rect)):
					seleccion = 2
		Boton1.update(window,Cursor1)
		Boton2.update(window,Cursor1)
		Cursor1.update()
		#Boton1.update(window,Cursor1)
		pygame.display.update()

	pygame.display.quit()
	return seleccion