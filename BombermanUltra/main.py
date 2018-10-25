import pygame
from character import Player
from mapCreation import GameMap
pygame.init()

window = pygame.display.set_mode((600,600))
pygame.display.set_caption("Bomberman Ultra")

Bomberman = Player()
mainLoop = True

mainMaze = GameMap(15,15,1)

mainMaze.printMaze()

while mainLoop:
	pygame.time.delay(100)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			mainLoop = False

	#Main movement handler
	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT]:
		Bomberman.posX -= Bomberman.vel
	if keys[pygame.K_RIGHT]:
		Bomberman.posX += Bomberman.vel
	if keys[pygame.K_UP]:
		Bomberman.posY -= Bomberman.vel
	if keys[pygame.K_DOWN]:
		Bomberman.posY += Bomberman.vel


	#Main map rendering
	mazeRender = mainMaze.getMaze()
	for i in mazeRender:
		for j in i:
			if j == 0: 
				pygame.draw.rect(window,(255,0,0),Bomberman.renderValues())
	pygame.display.update()

pygame.quit()