import pygame

def Victoria():
	winW,winH = 821,461

	window = pygame.display.set_mode((winW,winH))
	pygame.display.set_caption("Bomberman Ultra")
	fin = pygame.image.load("Terminar.jpg").convert_alpha()
	exit = 0
	while exit == 0:
		window.blit(fin,(0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = 1
		
		pygame.display.update()

	pygame.display.quit()